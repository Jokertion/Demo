#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: jokertion
@file: hospital.py
@time: 2020/3/3 19:30
@desc: 爬取微信小程序--腾讯健康的医疗救治点和发热门诊
"""
import json
import pymysql
import requests


def get_province_list():
    """
    获取省名和其中的城市数量
    :return: [{'province': '北京', 'city_count': 1}
    {'province': '河北', 'city_count': 11}]
    """
    url = "https://wechat.wecity.qq.com/api/THPneumoniaService/getHospitalProvince"

    payload = "{\"args\":{\"req\":{}},\"service\":\"THPneumoniaOuterService\",\"func\":\"getHospitalProvince\",\"context\":{\"channel\":\"AAGE4DTdkWHeoYS3T0Y8o3ZV\",\"userId\":\"486e8cce6dd64551b23034078182bd39\"}}"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        data_list = []
        pvs = json.loads(response.text, encoding='utf-8').get('args', {}).get('rsp', {}).get('provinces', {})
        for pv in pvs:
            pv_name = pv.get('provinceName')
            city_cnt = pv.get('cityCnt')
            temp = {'province': pv_name, 'city_count': city_cnt}
            data_list.append(temp)
        return json.dumps(data_list, ensure_ascii=False)


def get_cities_and_citycode(data_list):
    data_list = json.loads(data_list, encoding='utf-8')
    url = "https://wechat.wecity.qq.com/api/THPneumoniaService/getHospitalCityByProvince"

    for index, item in enumerate(data_list):
        prv = item.get('province')
        # TODO：参数中有中文的发送方法
        payload = {"args": {"req": {"province": prv}}, "service": "THPneumoniaOuterService",
                   "func": "getHospitalCityByProvince",
                   "context": {"channel": "AAGE4DTdkWHeoYS3T0Y8o3ZV", "userId": "486e8cce6dd64551b23034078182bd39"}}
        headers = {
            'Content-Type': 'application/json'
        }
        print('payload: ', payload)
        response = requests.post(url=url,
                                 headers=headers,
                                 data=json.dumps(payload, ensure_ascii=False).encode('utf-8'))
        print('response:', response.status_code, response.text)
        if response.status_code == 200:
            citys = json.loads(response.text, encoding='utf-8').get('args', {}).get('rsp', {}).get('info', {}).get(
                'citys', {})
            city_info = []
            for city in citys:
                areas = city.get('areas', [])
                # 根据有无areas分别抽取city和code信息
                if not areas:
                    city_code = city.get('cityCode')
                    city_name = city.get('cityName')
                    hsp_count = city.get('count')
                    temp = {'city_code': city_code, 'city_name': city_name, 'hsp_count': hsp_count}
                    city_info.append(temp)
                else:
                    for area in areas:
                        city_code = area.get('areaCode')
                        city_name = area.get('cityName')
                        hsp_count = area.get('count')
                        temp = {'city_code': city_code, 'city_name': city_name, 'hsp_count': hsp_count}
                        city_info.append(temp)
            data_list[index]['city_info'] = city_info
            print('--' * 100)
        # time.sleep(2)
    return json.dumps(data_list, ensure_ascii=False)


def get_hospital(data_list):
    data_list = json.loads(data_list, encoding='utf-8')
    for index, item in enumerate(data_list):
        city_info = item.get('city_info')
        for i, info in enumerate(city_info):
            city_code = info.get('city_code')
            if city_code:
                headers = {
                    'Content-Type': 'application/json'
                }
                params = (
                    ('cityCode', city_code),
                    ('pageIndex', '1'),
                    ('pageSize', '999'),
                    ('partnerType', '4'),
                    ('lat', '0'),
                    ('lng', 'undefined'),
                    ('searchKey', ''),
                )

                response = requests.get('https://card.wecity.qq.com/feverHosp/feverHospList', headers=headers,
                                        params=params)
                print(response.status_code, response.text)

                if response.status_code == 200:
                    hsp_data = json.loads(response.text, encoding='utf-8').get('data', {}).get('data', {})
                    data_list[index]['city_info'][i]['hsp_data'] = hsp_data
                    print(hsp_data)

    return json.dumps(data_list, ensure_ascii=False)


def save(data_list):
    db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='hospital')
    cursor = db.cursor()
    data_list = json.loads(data_list, encoding='utf-8')
    for index, dt in enumerate(data_list):
        province = dt.get('province')
        city_count = dt.get('city_count')
        city_info = dt.get('city_info')
        for i, info in enumerate(city_info):
            city_code = info.get('city_code')
            city_name = info.get('city_name')
            hsp_count = info.get('hsp_count')
            hsp_data = info.get('hsp_data')

            if hsp_data:
                for hsp in hsp_data:
                    hsp_name = hsp.get('orgName')
                    hsp_addr = hsp.get('orgAddr')
                    hsp_postcode = hsp.get('districtCode')
                    hsp_tel = hsp.get('hospitalTel')
                    is_fever = int(hsp.get('isFever', 0))
                    is_core = int(hsp.get('isCore', 0))

                    # 检查是否存过
                    check_sql = 'SELECT * FROM hospital where hsp_name = %s and hsp_addr = %s'
                    cursor.execute(check_sql, (hsp_name, hsp_addr))
                    rows = cursor.fetchone()
                    if not rows:
                        sql = 'INSERT INTO hospital(province, city_count, city_name, \
                        city_code, hsp_count, hsp_name, hsp_addr, hsp_postcode, hsp_tel, \
                        is_fever, is_core) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                        cursor.execute(sql, (province, city_count, city_name, city_code,
                                             hsp_count, hsp_name, hsp_addr, hsp_postcode,
                                             hsp_tel, is_fever, is_core))
                        db.commit()
                        print(f'【{hsp_name}】【{hsp_addr}】已存√')
                        print('--' * 100)
                    else:
                        print(f'【{hsp_name}】【{hsp_addr}】跑过啦')
                        print('--' * 100)


def main():
    data_list = get_province_list()
    data_list = get_cities_and_citycode(data_list)
    data_list = get_hospital(data_list)
    save(data_list)


if __name__ == '__main__':
    main()
