# ！ python3
# house.py
"""
题目：
1. 房子(House) 有 户型、总面积 和 家具名称列表
    --新房子没有任何的家具--
2. 家具(HouseItem) 有 名字 和 占地面积，其中
    席梦思(bed) 占地 4 平米
    衣柜(chest) 占地 2 平米
    餐桌(table) 占地 1.5 平米
3. 将以上三件 家具 添加 到 房子 中
4. 打印房子时，要求输出：户型、总面积、剩余面积、家具名称列表
"""


# 创建家具
class HouseItem:

    def __init__(self, name, area):
        self.name = name
        self.area = area

    def __str__(self):
        return '家具名称: %s\t占地面积: %s' % (self.name, self.area)


# 创建房子
class House:

    def __init__(self, house_type, area):
        self.area = area
        self.house_type = house_type

        # 初始剩余面积 = 总面积
        self.free_area = area
        # 初始家具列表
        self.item_list = []

    def __str__(self):
        return ('户型: %s\n总面积: %.2f[剩余: %.2f]\n家具:%s'
                % (self.house_type, self.area,
                   self.free_area, self.item_list))

    def add_item(self, item):
        # 1.判断家具大小，大了没法装进去
        if item.area > self.area:
            print('%s太大，%s平米的房子 放不进去哦' % (item.name, self.area))
            return
        # 2. 正常的话，添加家具名称到列表中
        self.item_list.append(item.name)
        # 3. 计算剩余面积
        self.free_area = self.free_area - item.area


# 创建家具实例
bed = HouseItem('席梦思', 4)
chest = HouseItem('衣柜', 200)
table = HouseItem('桌子', 1.5)
# print(bed)
# print(chest)
# print(table)

# 创建房子实例
my_house = House('两室一厅', 80, )
my_house.add_item(bed)
my_house.add_item(chest)
my_house.add_item(table)
print(my_house)
