# ！ python3
# score.py
"""
类方法、静态方法、实例方法 综合练习
需求:
设计一个 Game 类
属性：
定义一个 类属性 top_score 记录游戏的 历史最高分
定义一个 实例属性 player_name 记录 当前游戏的玩家姓名
方法：
静态方法 show_help 显示游戏帮助信息
类方法 show_top_score 显示历史最高分
实例方法 start_game 开始当前玩家的游戏
主程序步骤
1) 查看帮助信息
2) 查看历史最高分
3) 创建游戏对象，开始游戏
"""


class Game:
    top_score = 0

    def __init__(self, name):
        self.player_name = name

    @staticmethod
    def show_help():
        print('帮助信息：让僵尸吃掉你的脑袋')

    @classmethod
    def show_top_score(cls):
        print('历史最高分为：【%d】分' % cls.top_score)

    def start_game(self):
        print('开始 [%s] 的游戏' % self.player_name)
        Game.top_score = 3785


# 查看帮助信息
Game.show_help()

# 创建游戏对象，开始游戏
xm = Game('小明')
xm.start_game()

# 查看历史最高分
Game.show_top_score()
