#! python3

import sys
import json
import requests
import logging


# 从命令行参数获取位置
def recv_location():
    if len(sys.argv) < 2:
        print('Usage: weather 北京')
        sys.exit()
    location = str(sys.argv[1])
    logging.debug(location)
    main(location)


# 下载JSON数据
def main(location):
    # 获取数据JSON数据
    url = ' http://wthrcdn.etouch.cn/weather_mini?city=%s' % location
    response = requests.get(url)
    response.raise_for_status()

    # JSON文件格式转成Python格式
    weather_data = json.loads(response.text)

    # 字典原始数据如下
    # import pprint
    # pprint.pprint(weatherData)

    # 对字典数据进行处理
    w = weather_data['data']
    print('城市: {}\n'.format(w['city']))

    # 提取数据：日期 天气类型  最低温度 最高温度
    date = []
    weather_type = []
    low_temp = []
    high_temp = []
    forecast = w['forecast']

    # 存储数据，打印
    for i in range(len(forecast)):
        date.append(forecast[i]['date'])
        high_temp.append(forecast[i]['high'])
        low_temp.append(forecast[i]['low'])
        weather_type.append(forecast[i]['type'])
	
        print('日期: {} {}'.format(date[i][:-3], date[i][-3:]))
        print('天气: {}'.format(weather_type[i]))
        print('温度: {} ~{}\n\n'.format(low_temp[i][2:], high_temp[i][2:]))


if __name__ == '__main__':
    recv_location()
