#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Jokertion
@FileName: requests_mdpi_article_list.py
@Time: 2020/3/12  21:40
@Description:
"""

from lxml import html
import asyncio
import aiohttp
import aiomysql
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MONTH = {'Nov': '11',
         'Oct': '10',
         'Sep': '09',
         'Aug': '08',
         'Jul': '07',
         'Jun': '06',
         'May': '05',
         'Apr': '04',
         'Mar': '03',
         'Feb': '02',
         'Jan': '01',
         'Dec': '12'}
IGNORE_LIST = ['agronomy', 'animals']
HOST = "127.0.0.1"
USER = "root"
PASSWORD = "root"
DB = 'mdpi'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/76.0.3809.132 Safari/537.36',
    "Referer": 'https://www.mdpi.com/about/journals'
}


async def count_all_page(cur, journal):
    """
    从journals表中查出期刊应跑的数量，计算全部应跑页数
    :param cur: 游标
    :param journal: 期刊
    :return:
    """
    sql = 'SELECT total_nums FROM journals WHERE journal_name = %s '
    await cur.execute(sql, (journal,))
    total_nums = await cur.fetchone()
    total_nums = total_nums[0]
    page_num = int(total_nums) // 10 if int(total_nums) % 10 == 0 else int(total_nums) // 10 + 1
    return page_num


async def parse(cur, res, journal):
    """
    解析列表页
    :param cur:
    :param res:
    :param journal:
    :return:
    """
    # 列表页每一块的内容
    article_cons = res.xpath(
        "//div[@class='jscroll']/div[@class='generic-item article-item']/div[@class='article-content']")

    # 根据doi号是否存在判断是否需要更新此文章，有跳过，没有爬取
    for article_con in article_cons:
        doi_con = article_con.xpath("./div[@class='color-grey-dark']/a")
        if doi_con:
            publish_info = article_con.xpath("./div[@class='color-grey-dark']")[0].xpath('string()')
            doi = publish_info.split("doi.org/")[-1].split(" ")[0].strip()
            article_url = article_con.xpath("./a[@class='title-link']/@href")[0]
            publish_time = "".join([publish_info.split('-')[-1].strip().split(' ')[-1],
                                    MONTH.get(publish_info.split('-')[-1].strip().split(' ')[1]),
                                    publish_info.split('-')[-1].strip().split(' ')[0]])
            exist = await article_exist(cur, article_url)
            if exist:
                print(f"期刊:{journal}的文章{article_url}已在库中存在")
            else:
                insert_sql = '''insert into article_status(journal,doi,status,publish_time, article_url)
                                          values(%s, %s, %s, %s, %s)'''
                await cur.execute(insert_sql, (journal, doi, 0, publish_time, article_url))
                await cur.commit()
                print(f"存入√ 【{article_url}】【{doi}】【{publish_time}】")


async def send_request(session, url):
    """
    发送请求
    :param session:
    :param url:
    :return: response
    """
    while True:
        try:
            response = await session.get(url, headers=HEADERS, timeout=10)
            res = html.etree.HTML(await response.text())
            if response.status == 200:
                return res
            else:
                print('遇到特殊状态码: ', response.status)
                await asyncio.sleep(3)
        except Exception as e:
            print(e)
            await asyncio.sleep(3)


async def article_exist(cur, article_url):
    """
    判断文章是否跑过
    :param cur:
    :param article_url:
    :return:
    """
    check_sql = 'select id from article_status where article_url=%s'
    await cur.execute(check_sql, (article_url,))
    res = await cur.fetchone()
    if res:
        print(f"文章{article_url}已在库中存在")
        return True
    return False


async def screen_journal(cur):
    """
    筛选未跑完的期刊
    :return: all_journl_dict
    """
    select_journal = 'select * from journals'
    await cur.execute(select_journal)
    rows = await cur.fetchall()
    all_journl_dict = {}
    for index, row in enumerate(rows):
        journal = row[1]
        total_nums = int(row[4])
        all_journl_dict[journal] = total_nums
    return all_journl_dict


async def get_url_list(start_page_num, end_page_num, journal):
    """
    构造期刊所有列表页的url
    :param start_page_num:
    :param end_page_num:
    :param journal:
    :return:
    """
    url_list = []
    for page in range(start_page_num, end_page_num + 1):
        url = f'https://www.mdpi.com/search?sort=pubdate&page_no={page}&page_count=10&year_from=1996&year_to=2020&journal={journal}&view=default'
        url_list.append(url)
    return url_list


async def request_and_parse(session, cur, url, journal):
    """
    将请求和解析聚合
    :param session:
    :param cur:
    :param url:
    :param journal:
    :return:
    """
    res = await send_request(session, url)
    await parse(cur, res, journal)
    await asyncio.sleep(2)


async def do_something(session, cur, journal, url_list):
    """
    聚合协程 分配任务
    :param session:
    :param cur:
    :param journal:
    :param url_list:
    :return:
    """
    tasks = []
    for url in url_list:
        # 此处一定要使用create_task，不能直接await，否则不能并发运行
        task = asyncio.create_task(request_and_parse(session, cur, url, journal))
        tasks.append(task)

    # 等待所有任务执行完毕
    for task in tasks:
        await task


async def main():
    session = aiohttp.ClientSession()
    loop = asyncio.get_event_loop()
    try:
        conn = await aiomysql.connect(host=HOST, port=3306, user=USER, password=PASSWORD, db=DB, loop=loop)
        cur = await conn.cursor()
        journl_dict = await screen_journal(cur)
        for journal, pages in journl_dict.items():
            if journal in IGNORE_LIST:
                continue
            start_page_num = 1
            all_page_num = await count_all_page(cur, journal)
            url_list = await get_url_list(start_page_num, all_page_num, journal)
            await do_something(session, cur, journal, url_list)
    finally:
        loop.close()


if __name__ == '__main__':
    asyncio.run(main())
