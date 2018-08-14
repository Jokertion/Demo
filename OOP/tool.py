"""
类属性 类方法练习
需求:
定义一个 工具类
每件工具都有自己的 name
需求 —— 知道使用这个类，创建了多少个工具对象。
需求 —— 在 类 封装一个 show_tool_count 的类方法，输出使用当前这个类，创建的对象个数
"""


class Tools(object):

    count = 0

    def __init__(self, name):
        self.name = name
        Tools.count += 1

    @classmethod
    def show_tool_count(cls):
        print('当前类创建对象个数: %d' % cls.count)


fuzi = Tools('斧子')
chuizi = Tools('锤子')
liandao = Tools('镰刀')
# 调用类属性
# print('当前创建的对象个数:%d' % Tools.count)
# 调用类方法
Tools.show_tool_count()



