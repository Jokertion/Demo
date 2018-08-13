"""
OOP多态练习
需求：
在 Dog 类中封装方法 game
普通狗只是简单的玩耍
定义 XiaoTianDog 继承自 Dog，并且重写 game 方法
哮天犬需要在天上玩耍
定义 Person 类，并且封装一个 和狗玩 的方法
在方法内部，直接让 狗对象 调用 game 方法
"""


class Dog(object):

    def __init__(self, name):
        self.name = name

    def game(self):
        print('汪汪！%s冲 你翻跟头' % self.name)


class XiaoTianDog(Dog):

    def game(self):
        print('%s爱在天上玩耍' % self.name)


class Person(object):

    def __init__(self, name):
        self.name = name

    def paly_with_dog(self, dog):
        print('%s 和 %s 快乐的玩耍...'
              % (self.name, dog.name))
        dog.game()


# 1. 创建一个狗对象
bawanglong = Dog('霸王龙')
# bawanglong = XiaoTianDog('哮天犬')

# 2. 创建一个小明对象
xiaoming = Person('小明')

# 3. 让小明调用和狗玩的方法
xiaoming.paly_with_dog(bawanglong)


"""
多态：不同的子类对象调用相同的父类方法，产生不同的执行结果
总结：
1. Person 类中只需要让 狗对象 调用 game 方法，而不关心具体是 什么狗
    game 方法是在 Dog 父类中定义的
2. 在程序执行时，传入不同的 狗对象 实参，就会产生不同的执行效果
"""
