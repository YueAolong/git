#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本生成一个包含随机数字的文本文件，每行一个数字。
"""

import random
import os

def generate_numbers_file(filename, count=20, min_value=1, max_value=100):
    """
    生成一个包含随机数字的文本文件，每行一个数字
    
    参数:
        filename (str): 要创建的文件名
        count (int): 要生成的数字数量
        min_value (int): 随机数的最小值
        max_value (int): 随机数的最大值
    """
    with open(filename, 'w') as f:
        for _ in range(count):
            # 生成随机整数
            number = random.randint(min_value, max_value)
            # 写入文件，每行一个数字
            f.write(f"{number}\n")
    
    print(f"已生成包含 {count} 个随机数字的文件: {filename}")

if __name__ == "__main__":
    # 生成一个包含20个随机数字的文件
    generate_numbers_file("numbers.txt", 20, 1, 100) 