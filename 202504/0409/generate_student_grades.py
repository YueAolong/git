#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本生成一个包含学生姓名和成绩的CSV文件，使用UTF-8编码避免乱码。
"""

import csv
import random
import os

def generate_student_grades(filename, count=10, min_grade=60, max_grade=100):
    """
    生成一个包含学生姓名和成绩的CSV文件
    
    参数:
        filename (str): 要创建的文件名
        count (int): 要生成的学生数量
        min_grade (int): 最低成绩
        max_grade (int): 最高成绩
    """
    # 中文姓名列表
    first_names = ['张', '王', '李', '赵', '刘', '陈', '杨', '黄', '周', '吴']
    last_names = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军']
    
    # 使用UTF-8编码打开文件，并添加BOM标记以确保Excel正确识别编码
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        # 创建CSV写入器
        writer = csv.writer(f)
        
        # 写入表头
        writer.writerow(['姓名', '成绩'])
        
        # 生成学生数据
        for _ in range(count):
            # 随机生成姓名
            name = random.choice(first_names) + random.choice(last_names)
            # 随机生成成绩
            grade = random.randint(min_grade, max_grade)
            # 写入CSV
            writer.writerow([name, grade])
    
    print(f"已生成包含 {count} 个学生成绩的文件: {filename}")
    
    # 显示文件内容预览
    print("\n文件内容预览:")
    with open(filename, 'r', encoding='utf-8-sig') as f:
        for i, line in enumerate(f):
            if i < 5:  # 只显示前5行
                print(line.strip())
            else:
                break
    print("...")

if __name__ == "__main__":
    # 生成一个包含10个学生成绩的文件
    generate_student_grades("student_grades.csv", 10, 60, 100) 