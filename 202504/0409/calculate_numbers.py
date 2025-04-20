#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本读取包含数字的文本文件，计算数字的总和和平均值。
"""

import os
import sys

def calculate_sum_and_average(filename):
    """
    读取文件中的数字，计算总和和平均值
    
    参数:
        filename (str): 包含数字的文件名
        
    返回:
        tuple: (总和, 平均值, 数字列表)
    """
    if not os.path.exists(filename):
        print(f"错误: 文件 '{filename}' 不存在!")
        return None, None, None
    
    numbers = []
    total = 0
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                # 去除空白字符并转换为整数
                number = int(line.strip())
                numbers.append(number)
                total += number
        
        # 计算平均值
        average = total / len(numbers) if numbers else 0
        
        return total, average, numbers
    
    except ValueError as e:
        print(f"错误: 文件包含非数字内容: {e}")
        return None, None, None
    except Exception as e:
        print(f"错误: 读取文件时发生错误: {e}")
        return None, None, None

def display_results(filename):
    """
    显示计算结果
    
    参数:
        filename (str): 包含数字的文件名
    """
    total, average, numbers = calculate_sum_and_average(filename)
    
    if total is None:
        return
    
    print(f"\n文件 '{filename}' 的分析结果:")
    print(f"数字列表: {numbers}")
    print(f"数字个数: {len(numbers)}")
    print(f"数字总和: {total}")
    print(f"数字平均值: {average:.2f}")

if __name__ == "__main__":
    # 默认文件名
    filename = "numbers.txt"
    
    # 如果提供了命令行参数，使用它作为文件名
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    display_results(filename) 