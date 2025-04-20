#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本演示了向文本文件中写入学生成绩，并确保文件被正确保存。
"""

import os
import time
from datetime import datetime

def write_grades_to_file(filename, grades_data):
    """
    将学生成绩写入文本文件
    
    参数:
        filename (str): 文件名
        grades_data (dict): 包含学生姓名和成绩的字典
    """
    print(f"正在将学生成绩写入文件 '{filename}'...")
    
    try:
        # 使用with语句确保文件正确关闭
        with open(filename, 'w', encoding='utf-8') as file:
            # 写入文件头
            file.write("学生成绩单\n")
            file.write("=" * 20 + "\n")
            file.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("=" * 20 + "\n\n")
            
            # 写入表头
            file.write(f"{'姓名':<10}{'成绩':<10}{'等级':<10}\n")
            file.write("-" * 30 + "\n")
            
            # 写入学生成绩
            for student, grade in grades_data.items():
                # 根据成绩确定等级
                if grade >= 90:
                    level = "优秀"
                elif grade >= 80:
                    level = "良好"
                elif grade >= 70:
                    level = "中等"
                elif grade >= 60:
                    level = "及格"
                else:
                    level = "不及格"
                
                # 写入一行数据
                file.write(f"{student:<10}{grade:<10}{level:<10}\n")
            
            # 计算并写入统计信息
            file.write("\n" + "=" * 20 + "\n")
            file.write("统计信息:\n")
            file.write(f"学生总数: {len(grades_data)}\n")
            file.write(f"平均分: {sum(grades_data.values()) / len(grades_data):.2f}\n")
            file.write(f"最高分: {max(grades_data.values())}\n")
            file.write(f"最低分: {min(grades_data.values())}\n")
        
        # 验证文件是否成功保存
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"文件已成功保存! 文件大小: {file_size} 字节")
            return True
        else:
            print("错误: 文件未能成功保存!")
            return False
            
    except Exception as e:
        print(f"写入文件时发生错误: {e}")
        return False

def read_file_to_verify(filename):
    """
    读取文件内容以验证写入是否成功
    
    参数:
        filename (str): 文件名
    """
    print(f"\n验证文件 '{filename}' 内容:")
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
        return True
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return False

def main():
    """
    主函数，演示写入学生成绩到文件
    """
    # 创建学生成绩数据
    student_grades = {
        "张三": 85,
        "李四": 92,
        "王五": 78,
        "赵六": 95,
        "钱七": 88,
        "孙八": 76,
        "周九": 90,
        "吴十": 82
    }
    
    # 文件名
    filename = "student_grades.txt"
    
    # 写入成绩到文件
    if write_grades_to_file(filename, student_grades):
        # 验证文件内容
        read_file_to_verify(filename)
        
        # 演示追加内容到文件
        print("\n正在向文件追加新学生成绩...")
        try:
            with open(filename, 'a', encoding='utf-8') as file:
                file.write("\n" + "=" * 20 + "\n")
                file.write("追加的学生成绩:\n")
                file.write(f"{'姓名':<10}{'成绩':<10}{'等级':<10}\n")
                file.write("-" * 30 + "\n")
                
                # 追加新学生
                new_students = {
                    "郑十一": 87,
                    "王十二": 93
                }
                
                for student, grade in new_students.items():
                    if grade >= 90:
                        level = "优秀"
                    elif grade >= 80:
                        level = "良好"
                    elif grade >= 70:
                        level = "中等"
                    elif grade >= 60:
                        level = "及格"
                    else:
                        level = "不及格"
                    
                    file.write(f"{student:<10}{grade:<10}{level:<10}\n")
            
            print("已成功追加新学生成绩!")
            
            # 再次验证文件内容
            read_file_to_verify(filename)
            
        except Exception as e:
            print(f"追加内容时发生错误: {e}")
    
    print("\n文件操作演示完成!")

if __name__ == "__main__":
    main() 