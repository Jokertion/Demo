# ! python3
# date_account.py
# 爱情计算器:知日期求间隔,知间隔求日期
import datetime
import time


# 知日期求间隔
class Interval:

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def now_to_date(self):
        # 从现在时间计算：
        # start = datetime.datetime.fromtimestamp(time.time())
        # 从指定日期计算：
        start = datetime.datetime(2017, 1, 8, 0, 37, 0)

        print('恋爱开始时间:【%s】【丙申年腊月十一日零点三十七分】' % start.strftime('%Y/%m/%d %H:%M:%S'))

        # 计算时间差
        end = datetime.datetime(self.year, self.month, self.day)
        interval = end - start

        # 修剪打印内容
        # print(str(interval))
        interval = str(interval).split('days,')
        day = interval[0]
        hours = interval[1].split('.')[0]
        hour, minute, second = hours.split(':')[0:3]
        now = str(datetime.datetime.fromtimestamp(time.time())).split('.')[0]

        print('现在时刻:【%s】\n在一起：【%s】天 【%s】小时【%s】分【%s】秒'
              % (now, day.strip(), hour.strip(), minute, second))


# 知间隔求日期
class Date:

    def __init__(self, days):
        self.days = days

    def now_and_delta(self):
        # 从当前时间开始计算：
        # start = datetime.datetime.fromtimestamp(time.time())

        # 从指定时间开始计算：
        start = datetime.datetime(2017, 1, 8, 0, 37, 0)

        # print('开始时间:【%s】' % start.strftime('%Y-%m-%d %H:%M:%S'))
        date = start + datetime.timedelta(self.days)
        date = str(date).split()[0]
        print('恋爱%s天是:【%s】' % (self.days, date))


# 知日期求间隔
# date1 = Interval(2018, 9, 16)
date1 = Interval(2018, 8, 13)
date1.now_to_date()
print('*' * 50)
# 知间隔求日期
date2 = Date(600)
date3 = Date(1000)
date4 = Date(2000)
date5 = Date(5000)
date6 = Date(10000)
date7 = Date(25000)

date2.now_and_delta()
date3.now_and_delta()
date4.now_and_delta()
date5.now_and_delta()
date6.now_and_delta()
date7.now_and_delta()
print('到这一天，我92岁，如果依然活着，愿爱你如初')
print('*' * 50)
