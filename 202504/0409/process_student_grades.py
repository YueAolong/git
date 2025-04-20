#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本读取学生成绩文件，将数据存储到字典中，并计算每个学生的成绩及班级平均成绩。
"""

import csv
import os
import sys
import statistics

def read_student_grades(filename):
    """
    读取学生成绩文件，将数据存储到字典中
    
    参数:
        filename (str): 包含学生成绩的文件名
        
    返回:
        dict: 包含学生成绩的字典，格式为 {学生姓名: 成绩}
    """
    if not os.path.exists(filename):
        print(f"错误: 文件 '{filename}' 不存在!")
        return None
    
    student_grades = {}
    
    try:
        # 使用UTF-8编码打开文件
        with open(filename, 'r', encoding='utf-8-sig') as f:
            # 创建CSV读取器
            reader = csv.reader(f)
            
            # 跳过表头
            next(reader)
            
            # 读取学生数据
            for row in reader:
                if len(row) >= 2:
                    name = row[0]
                    grade = int(row[1])
                    student_grades[name] = grade
        
        return student_grades
    
    except ValueError as e:
        print(f"错误: 文件包含非数字成绩: {e}")
        return None
    except Exception as e:
        print(f"错误: 读取文件时发生错误: {e}")
        return None

def calculate_statistics(student_grades):
    """
    计算班级统计信息
    
    参数:
        student_grades (dict): 包含学生成绩的字典
        
    返回:
        dict: 包含统计信息的字典
    """
    if not student_grades:
        return None
    
    grades = list(student_grades.values())
    
    stats = {
        'count': len(student_grades),
        'total': sum(grades),
        'average': statistics.mean(grades),
        'median': statistics.median(grades),
        'min': min(grades),
        'max': max(grades)
    }
    
    return stats

def display_results(filename):
    """
    显示分析结果
    
    参数:
        filename (str): 包含学生成绩的文件名
    """
    # 读取学生成绩
    student_grades = read_student_grades(filename)
    
    if student_grades is None:
        return
    
    # 计算统计信息
    stats = calculate_statistics(student_grades)
    
    if stats is None:
        return
    
    print(f"\n文件 '{filename}' 的分析结果:")
    print(f"学生人数: {stats['count']}")
    print(f"成绩总和: {stats['total']}")
    print(f"班级平均成绩: {stats['average']:.2f}")
    print(f"中位成绩: {stats['median']:.2f}")
    print(f"最低成绩: {stats['min']}")
    print(f"最高成绩: {stats['max']}")
    
    # 显示所有学生成绩
    print("\n学生成绩列表:")
    print("姓名\t成绩\t与平均分的差距")
    print("-" * 35)
    for name, grade in student_grades.items():
        diff = grade - stats['average']
        diff_str = f"+{diff:.2f}" if diff > 0 else f"{diff:.2f}"
        print(f"{name}\t{grade}\t{diff_str}")
    
    # 按成绩排序
    sorted_students = sorted(student_grades.items(), key=lambda x: x[1], reverse=True)
    
    print("\n成绩排名:")
    print("排名\t姓名\t成绩")
    print("-" * 20)
    for i, (name, grade) in enumerate(sorted_students, 1):
        print(f"{i}\t{name}\t{grade}")

if __name__ == "__main__":
    # 默认文件名
    filename = "student_grades.csv"
    
    # 如果提供了命令行参数，使用它作为文件名
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    display_results(filename) 