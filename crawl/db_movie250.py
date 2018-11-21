# request + bs4 + MongoDB 豆瓣电影爬虫
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


def crawl_db_movie():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)\
        AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/69.0.3497.100 Safari/537.36",
        "Host": "movie.douban.com"
    }

    movie_lst = []
    for i in range(2):
        url = "https://movie.douban.com/top250?start={}&filter=".format(str(i * 25))
        response = requests.get(url, headers=headers)
        # print(response.text)

        soup = BeautifulSoup(response.text, "lxml")

        div_info = soup.find_all('div', {'class': 'item'})
        # print(div_info)

        for node in div_info:
            rank = node.find('em', {'class': ''}).text
            name = node.find('div', {'class': 'info'}).find('a').find('span').text
            point = node.find('span', {'class': 'rating_num'}).text + '分'
            quote = node.find('span', {'class': 'inq'}).text

            # MongoDB数据库只能插入字典类型的数据，所以要将信息以键值对的形式保存到一个字典中
            data_dict = {
                '排名': rank,
                '影名': name,
                '评分': point,
                '评语': quote,
            }

            movie_lst.append(data_dict)

    return movie_lst


def save_to_mongodb(data):
    for dic in data:
        collection.insert_one(dic)


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.spider
    collection = db.movie250

    data_lst = crawl_db_movie()

    # save_to_mongodb(data_lst)

    cursor = collection.find({'评分': '9.5分'})
    for doc in cursor:
        print(doc)

    # collection.delete_many({})
