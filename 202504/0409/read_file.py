#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本演示了多种读取文件并打印文件内容的方法。
"""

def read_file_method1(filename):
    """
    方法1：使用open()函数和read()方法读取整个文件
    """
    print(f"\n方法1 - 使用read()方法读取整个文件 '{filename}':")
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 不存在")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

def read_file_method2(filename):
    """
    方法2：使用open()函数和readlines()方法逐行读取文件
    """
    print(f"\n方法2 - 使用readlines()方法逐行读取文件 '{filename}':")
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                print(line, end='')  # end='' 避免打印额外的换行符
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 不存在")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

def read_file_method3(filename):
    """
    方法3：使用for循环直接遍历文件对象
    """
    print(f"\n方法3 - 使用for循环直接遍历文件对象 '{filename}':")
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                print(line, end='')
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 不存在")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

def read_file_method4(filename):
    """
    方法4：使用with语句和readline()方法逐行读取文件
    """
    print(f"\n方法4 - 使用readline()方法逐行读取文件 '{filename}':")
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                print(line, end='')
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 不存在")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

def read_file_method5(filename):
    """
    方法5：读取文件并统计行数、字符数等信息
    """
    print(f"\n方法5 - 读取文件 '{filename}' 并统计信息:")
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.splitlines()
            line_count = len(lines)
            char_count = len(content)
            word_count = len(content.split())
            
            print(f"文件内容:")
            print(content)
            print(f"\n文件统计信息:")
            print(f"行数: {line_count}")
            print(f"字符数: {char_count}")
            print(f"单词数: {word_count}")
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 不存在")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

def main():
    """
    主函数，演示所有读取文件的方法
    """
    # 创建一个示例文件
    sample_filename = "sample.txt"
    try:
        with open(sample_filename, 'w', encoding='utf-8') as file:
            file.write("这是第一行。\n")
            file.write("这是第二行。\n")
            file.write("这是第三行。\n")
            file.write("这是第四行。\n")
            file.write("这是第五行。\n")
        print(f"已创建示例文件 '{sample_filename}'")
    except Exception as e:
        print(f"创建示例文件时发生错误: {e}")
        return
    
    # 演示所有读取文件的方法
    read_file_method1(sample_filename)
    read_file_method2(sample_filename)
    read_file_method3(sample_filename)
    read_file_method4(sample_filename)
    read_file_method5(sample_filename)
    
    # 演示读取不存在的文件
    nonexistent_file = "nonexistent.txt"
    read_file_method1(nonexistent_file)
    
    print("\n所有文件读取方法演示完成！")

if __name__ == "__main__":
    main() 