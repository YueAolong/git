#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本允许用户选择一个文件，然后读取文件内容，提取文件中的数字，并计算这些数字的总和。
"""

import re
import os
import sys

def list_files_in_directory(directory="."):
    """
    列出指定目录中的所有文件
    
    参数:
        directory (str): 目录路径，默认为当前目录
        
    返回:
        list: 文件列表
    """
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return files
    except Exception as e:
        print(f"列出目录文件时发生错误: {e}")
        return []

def select_file():
    """
    让用户选择一个文件
    
    返回:
        str: 选择的文件路径
    """
    # 列出当前目录中的所有文件
    files = list_files_in_directory()
    
    if not files:
        print("当前目录中没有文件!")
        return None
    
    # 显示文件列表
    print("\n当前目录中的文件:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    
    # 让用户选择文件
    while True:
        try:
            choice = input("\n请选择文件编号 (输入'q'退出): ")
            
            if choice.lower() == 'q':
                return None
            
            choice = int(choice)
            if 1 <= choice <= len(files):
                return files[choice - 1]
            else:
                print(f"无效的选择! 请输入1到{len(files)}之间的数字。")
        except ValueError:
            print("无效的输入! 请输入数字或'q'。")

def calculate_sum_from_file(filename):
    """
    读取文件内容，提取数字并计算总和
    
    参数:
        filename (str): 文件名
        
    返回:
        tuple: (总和, 数字列表)
    """
    print(f"正在从文件 '{filename}' 中提取数字并计算总和...")
    
    if not os.path.exists(filename):
        print(f"错误: 文件 '{filename}' 不存在!")
        return 0, []
    
    numbers = []
    total_sum = 0
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # 使用正则表达式提取所有数字（包括整数、小数、负数和科学计数法）
            number_pattern = r'-?\d+\.?\d*e?[+-]?\d*'
            found_numbers = re.findall(number_pattern, content)
            
            # 将提取的字符串转换为浮点数
            for num_str in found_numbers:
                try:
                    num = float(num_str)
                    numbers.append(num)
                    total_sum += num
                except ValueError:
                    print(f"警告: 无法将 '{num_str}' 转换为数字，已跳过")
        
        print(f"从文件中提取了 {len(numbers)} 个数字")
        print(f"数字列表: {numbers}")
        print(f"数字总和: {total_sum}")
        
        return total_sum, numbers
    
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return 0, []

def calculate_sum_by_line(filename):
    """
    按行读取文件，提取每行中的数字并计算总和
    
    参数:
        filename (str): 文件名
        
    返回:
        dict: 每行的数字和总和
    """
    print(f"\n按行读取文件 '{filename}' 并计算每行的数字总和...")
    
    if not os.path.exists(filename):
        print(f"错误: 文件 '{filename}' 不存在!")
        return {}
    
    line_sums = {}
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                # 使用正则表达式提取当前行中的所有数字
                number_pattern = r'-?\d+\.?\d*e?[+-]?\d*'
                found_numbers = re.findall(number_pattern, line)
                
                # 将提取的字符串转换为浮点数
                line_numbers = []
                line_sum = 0
                
                for num_str in found_numbers:
                    try:
                        num = float(num_str)
                        line_numbers.append(num)
                        line_sum += num
                    except ValueError:
                        print(f"警告: 第 {line_num} 行中无法将 '{num_str}' 转换为数字，已跳过")
                
                # 存储当前行的数字和总和
                line_sums[line_num] = {
                    'numbers': line_numbers,
                    'sum': line_sum
                }
                
                # 打印当前行的结果
                print(f"第 {line_num} 行: 数字 {line_numbers}, 总和 {line_sum}")
        
        return line_sums
    
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return {}

def create_sample_file(filename):
    """
    创建一个包含数字的示例文件
    
    参数:
        filename (str): 文件名
    """
    print(f"正在创建示例文件 '{filename}'...")
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("这是一个包含各种数字的示例文件。\n")
            file.write("第一行: 10, 20, 30\n")
            file.write("第二行: 40 50 60\n")
            file.write("第三行: 70.5, 80.5, 90.5\n")
            file.write("第四行: 100\n")
            file.write("第五行: 这是一个文本，不包含数字\n")
            file.write("第六行: 这里有数字123和456\n")
            file.write("第七行: 负数-10和-20\n")
            file.write("第八行: 科学计数法1.23e-4和5.67e+8\n")
        
        print(f"示例文件 '{filename}' 已创建成功!")
        return True
    except Exception as e:
        print(f"创建示例文件时发生错误: {e}")
        return False

def main():
    """
    主函数，让用户选择文件并计算数字总和
    """
    print("=== 文件数字总和计算器 ===")
    
    # 询问用户是否需要创建示例文件
    create_sample = input("是否需要创建示例文件? (y/n): ").lower()
    
    if create_sample == 'y':
        sample_filename = "sample_numbers.txt"
        if create_sample_file(sample_filename):
            print(f"示例文件 '{sample_filename}' 已创建，您可以在文件列表中选择它。")
    
    # 让用户选择文件
    selected_file = select_file()
    
    if selected_file:
        # 计算文件中所有数字的总和
        total_sum, all_numbers = calculate_sum_from_file(selected_file)
        
        # 按行计算数字总和
        line_sums = calculate_sum_by_line(selected_file)
        
        # 计算所有行的总和
        total_line_sum = sum(line_info['sum'] for line_info in line_sums.values())
        print(f"\n所有行的数字总和: {total_line_sum}")
        
        # 验证两种方法计算的总和是否一致
        if abs(total_sum - total_line_sum) < 1e-10:  # 考虑浮点数精度
            print("验证成功: 两种方法计算的总和一致!")
        else:
            print(f"警告: 两种方法计算的总和不一致! 方法1: {total_sum}, 方法2: {total_line_sum}")
    else:
        print("未选择文件，程序退出。")
    
    print("\n程序执行完成!")

if __name__ == "__main__":
    main() 