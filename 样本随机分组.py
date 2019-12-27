#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


def sample_divided_by_random(sample_list, groups=2):
    """
    样本随机分组--升级版
    :param sample_list:  样本列表
    :param groups: 组数，默认两组
    :return: 随机分好组的样本列表
    """
    dic = {}
    each_group_nums = len(sample_list) // groups
    dict_key = range(1, groups + 1)
    for k in dict_key:
        value = []
        for i in range(each_group_nums):
            p = random.choice(sample_list)
            sample_list.remove(p)
            value.append(p)
        dic[k] = value

    for k, v in dic.items():
        print(f'第{k}组: {v}')


if __name__ == '__main__':
    t = [2, 4, 5, 8, 11, 60, 47, 32, 15, 44, 30, 83]
    sample_divided_by_random(t)

