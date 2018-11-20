import os


def c_name(path):
    # os.listdir()遍历文件夹内的每个文件名，并返回一个包含文件名的list
    for file in os.listdir(path):
        new_name = file.split('：')[1].split('[高清版]')[0] + '.flv'
        # rename之前要先用chdir()函数进入到目标文件所在的路径
        os.chdir(path)
        os.rename(file, new_name)


if __name__ == '__main__':
    path = 'C:\\Users\\Administrator\\Desktop\\崔庆才爬虫视频'
    c_name()
