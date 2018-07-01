import time
def outer(func):
	def inner():
		start_time = time.time()
		func()
		stop_time = time.time()
		print('用装饰器统计函数运行时间:%f'
			%(stop_time-start_time))
	return inner

@outer
def foo():
	print("业务")
	sum = 0
	for i in range(10000):
		sum += i
	print(sum)

foo()
