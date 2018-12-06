# -*- coding:utf-8 -*-
from lxml import etree
import requests
import json
import threading
from queue import Queue


CRAWL_EXIT = False


class ThreadCrawl(threading.Thread):

    def __init__(self, thread_name, page_queue, data_queue):
        threading.Thread.__init__(self)
        self.thread_name = thread_name  # 线程名
        self.page_queue = page_queue  # 页码队列
        self.data_queue = data_queue  # 数据队列
        self.headers = '"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",\
            "Referer": "https://www.qiushibaike.com/",\
            "Host": "www.qiushibaike.com",\
            "Upgrade-Insecure-Requests": "1",'

    def run(self):
        print('启动 ' + self.thread_name)
        while not CRAWL_EXIT:
            try:
                # 从data_queue 中取出一个页码数字，先进先出
                # 可选参数block，默认是True
                # 如果队列为空，block为True，会进入阻塞状态，直到队列有新的数据
                # 如果队列为空，block为False，会弹出一个Queue.empty()异常
                page = self.page_queue.get(False)

                # 构建网页的 URL 地址
                url = "http://www.qiushibaike.com/8hr/page/" + str(page) + "/"
                content = requests.get(url, headers=self.headers).text

                # 将爬到的网页源代码放入到data_queue队列中
                self.data_queue.put(content)
            except:
                pass
        print("结束 " + self.thread_name)


PARSE_EXIT = False


class ThreadPrased(threading.Thread):

    def __init__(self, thread_name, data_queue, local_file, lock):
        super(ThreadPrased, self).__init__()
        # 线程名
        self.thread_name = thread_name
        # 数据队列
        self.data_queue = data_queue
        # 保存解析后的数据文件名
        self.local_file = local_file
        # 互斥锁
        self.lock = lock

    def run(self):
        print("启动 " + self.thread_name)
        while not PARSE_EXIT:
            try:
                html = self.data_queue.get(False)
                self.parse(html)
            except:
                pass
        print("结束 " + self.thread_name)

    def parse(self, html):
        # 返回所有段子的结点位置
        text = etree.HTML(html)
        # contains 模糊查询，第一个参数是要匹配的标签，第二个参数是标签名的部分内容
        node_list = text.xpath('//div[contains(@id,"qiushi_tag")]')

        for node in node_list:
            username = node.xpath('./div')[0].xpath(".//h2")[0].text
            image = node.xpath('.//div[@class="thumb"]//@src')
            content = node.xpath('.//div[@class="content"]/span')[0].text
            # like = node.xpath('.//div[@class="stats"]/span/i').text
            like = node.xpath('.//i')[0].text
            comments = node.xpath('.//i')[1].text

            items = {
                "username": username.replace('\n', ''),
                "content": content.replace('\n', ''),
                "image": image,
                "like": like,
                "comments": comments,
            }
            # with 后面有两个必须执行的操作：__enter__ 和 __exit__ ，打开和关闭
            # 不管里面的操作如何， 都会直接打开和关闭功能
            # 打开锁，向文件添加内容，释放锁
            with self.lock:
                # 写入解析后的数据
                self.local_file.write(json.dumps(items, ensure_ascii=False) + "\n")


def main():
    # 页码队列，存储20个页码，先进先出
    page_queue = Queue(20)
    for i in range(20):
        page_queue.put(i)

    # 采集结果(网页的 HTML 源代码) 的数据队列，参数为空表示不限制
    data_queue = Queue()
    # 以追加的方式打开本地文件
    local_file = open("duanzi_thread.json", "a")
    # 互斥锁
    lock = threading.Lock()

    # 3个采集线程的名字
    crawl_list = ['线程采集1号', '线程采集2号', '线程采集3号']
    # 创建、启动和存储3个采集线程
    thread_crawls = []
    for thread_name in crawl_list:
        thread = ThreadCrawl(thread_name, page_queue, data_queue)
        thread.start()
        thread_crawls.append(thread)

    # 3个解析线程的名字
    parse_list = ['解析线程1号', '解析线程2号', '解析线程3号']
    # 创建、启动和存储三个解析线程
    thread_parse = []
    for thread_name in parse_list:
        thread = ThreadPrased(thread_name, data_queue, local_file, lock)
        thread.start()
        thread_parse.append(thread)

    # 采集线程相关的控制
    while not page_queue.empty():
        pass
    # 如果page_queue为空，采集线程退出循环
    global CRAWL_EXIT
    CRAWL_EXIT = True
    print('page_queue为空')
    for thread in thread_crawls:
        thread.join()  # 阻塞子线程

    # 解析线程相关的控制
    while not data_queue.empty():
        pass
    print("data_queue为空")
    global PARSE_EXIT
    PARSE_EXIT = True
    for thread in thread_parse:
        thread.join()

    with lock:
        # 关闭文件，在关闭之前，内容都存在内存里
        local_file.close()


if __name__ == '__main__':
    main()
