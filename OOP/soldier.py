# ！ python3
# soldier.py
"""
封装练习2--枪与士兵
需求：
1. 士兵 许三多 有一把 AK47
2. 士兵 可以 开火
3. 枪 能够 发射 子弹
4. 枪 装填 装填子弹 —— 增加子弹数量
"""


class Gun:

    def __init__(self, model):
        self.model = model
        self.num = 0

    def __str__(self):
        return ('枪型: %s\t子弹剩余数量: [%d]颗 '
                % (self.model, self.num))

    def shoot(self):
        # 判断子弹数量是否大于1
        if self.num < 3:
            print(self)
            print('子弹数量不足...')
            return
        self.num -= 3
        print('嘟嘟嘟...')

    def add_bullet(self, count):
        self.num += count


class Soldier:

    def __init__(self, name):
        self.name = name
        self.gun = None

    def fire(self):
        if self.gun is None:
            print('%s还没有枪呢!' % self.name)
            return
        print('为了新中国的胜利，冲啊！')
        self.gun.shoot()


ak47 = Gun('AK47')
xsd = Soldier('许三多')
# 给xsd配枪
xsd.gun = ak47
# 上子弹
ak47.add_bullet(50)
xsd.fire()
xsd.fire()
# 查询枪剩余子弹数
print(ak47)
