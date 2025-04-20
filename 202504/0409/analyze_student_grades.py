#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本读取学生成绩CSV文件，计算统计信息并显示结果。
"""

import csv
import os
import sys
import statistics

def analyze_student_grades(filename):
    """
    读取学生成绩CSV文件，计算统计信息
    
    参数:
        filename (str): 包含学生成绩的CSV文件名
        
    返回:
        dict: 包含统计信息的字典
    """
    if not os.path.exists(filename):
        print(f"错误: 文件 '{filename}' 不存在!")
        return None
    
    students = []
    grades = []
    
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
                    students.append({'name': name, 'grade': grade})
                    grades.append(grade)
        
        # 计算统计信息
        stats = {
            'count': len(students),
            'total': sum(grades),
            'average': statistics.mean(grades),
            'median': statistics.median(grades),
            'min': min(grades),
            'max': max(grades),
            'students': students
        }
        
        return stats
    
    except ValueError as e:
        print(f"错误: 文件包含非数字成绩: {e}")
        return None
    except Exception as e:
        print(f"错误: 读取文件时发生错误: {e}")
        return None

def display_results(filename):
    """
    显示分析结果
    
    参数:
        filename (str): 包含学生成绩的CSV文件名
    """
    stats = analyze_student_grades(filename)
    
    if stats is None:
        return
    
    print(f"\n文件 '{filename}' 的分析结果:")
    print(f"学生人数: {stats['count']}")
    print(f"成绩总和: {stats['total']}")
    print(f"平均成绩: {stats['average']:.2f}")
    print(f"中位成绩: {stats['median']:.2f}")
    print(f"最低成绩: {stats['min']}")
    print(f"最高成绩: {stats['max']}")
    
    # 显示所有学生成绩
    print("\n学生成绩列表:")
    print("姓名\t成绩")
    print("-" * 15)
    for student in stats['students']:
        print(f"{student['name']}\t{student['grade']}")
    
    # 按成绩排序
    sorted_students = sorted(stats['students'], key=lambda x: x['grade'], reverse=True)
    
    print("\n成绩排名:")
    print("排名\t姓名\t成绩")
    print("-" * 20)
    for i, student in enumerate(sorted_students, 1):
        print(f"{i}\t{student['name']}\t{student['grade']}")

if __name__ == "__main__":
    # 默认文件名
    filename = "student_grades.csv"
    
    # 如果提供了命令行参数，使用它作为文件名
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    display_results(filename) 