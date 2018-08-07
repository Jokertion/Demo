#! python3

import sys
import json
import requests
import pprint
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

# 从命令行参数获取位置
def recv_location():
	if len(sys.argv) < 2:
		print('Usage: quickWeather.py location')
		sys.exit()
	location = str(sys.argv[1])
	logging.debug(location)

	main(location)
	
# 下载JSON数据
def main(location):
	logging.debug('你好URL')
	# url = ' http://wthrcdn.etouch.cn/weather_mini?city=%s' % location
	url = ' http://wthrcdn.etouch.cn/weather_mini?city=%s' % (location)
	response = requests.get(url)
	response.raise_for_status()

	# JSON文件格式转成Python格式
	weatherData = json.loads(response.text)
	# pprint.pprint(weatherData)

	# 对字典数据进行处理
	w = weatherData['data']
	print('城市: {}\n'.format(w['city']))

	forecast = w['forecast']
	date = []
	high_temp = []
	low_temp = []
	type = []

	for i in range(len(forecast)):
		date.append(forecast[i]['date'])
		high_temp.append(forecast[i]['high'])
		low_temp.append(forecast[i]['low'])
		type.append(forecast[i]['type'])

		print('日期: {} {}'.format(date[i][:-3], date[i][-3:]))
		print('天气: {}'.format(type[i]))
		print('温度: {} ~{}\n\n'.format(low_temp[i][2:],high_temp[i][2:]))

		
if __name__ == '__main__':
	recv_location()