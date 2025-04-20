#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本读取学生成绩文件，进行全面的统计分析，并生成可视化图表和导出分析结果。
"""

import csv
import os
import sys
import statistics
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def read_student_data(filename):
    """
    读取学生成绩文件，将数据存储到字典和DataFrame中
    
    参数:
        filename (str): 包含学生成绩的文件名
        
    返回:
        tuple: (字典格式的学生数据, DataFrame格式的学生数据)
    """
    if not os.path.exists(filename):
        print(f"错误: 文件 '{filename}' 不存在!")
        return None, None
    
    student_dict = {}
    
    try:
        # 使用pandas读取CSV文件
        df = pd.read_csv(filename, encoding='utf-8-sig')
        
        # 同时创建字典格式
        for _, row in df.iterrows():
            student_dict[row['姓名']] = row['成绩']
        
        return student_dict, df
    
    except Exception as e:
        print(f"错误: 读取文件时发生错误: {e}")
        return None, None

def calculate_statistics(student_dict, df):
    """
    计算详细的统计信息
    
    参数:
        student_dict (dict): 包含学生成绩的字典
        df (DataFrame): 包含学生成绩的DataFrame
        
    返回:
        dict: 包含统计信息的字典
    """
    if not student_dict or df is None:
        return None
    
    grades = list(student_dict.values())
    
    # 基本统计量
    stats = {
        'count': len(student_dict),
        'total': sum(grades),
        'average': statistics.mean(grades),
        'median': statistics.median(grades),
        'min': min(grades),
        'max': max(grades),
        'std_dev': statistics.stdev(grades) if len(grades) > 1 else 0,
        'variance': statistics.variance(grades) if len(grades) > 1 else 0
    }
    
    # 计算百分位数
    stats['percentile_25'] = statistics.quantiles(grades, n=4)[0]
    stats['percentile_75'] = statistics.quantiles(grades, n=4)[2]
    
    # 计算成绩分布
    bins = [0, 60, 70, 80, 90, 100]
    labels = ['不及格', '及格', '良好', '优秀', '满分']
    df['成绩等级'] = pd.cut(df['成绩'], bins=bins, labels=labels, right=True)
    
    grade_distribution = df['成绩等级'].value_counts().to_dict()
    stats['grade_distribution'] = grade_distribution
    
    # 计算及格率
    passing_count = sum(1 for grade in grades if grade >= 60)
    stats['passing_rate'] = passing_count / len(grades) * 100
    
    return stats

def generate_visualizations(df, stats, output_dir='charts'):
    """
    生成可视化图表
    
    参数:
        df (DataFrame): 包含学生成绩的DataFrame
        stats (dict): 包含统计信息的字典
        output_dir (str): 图表输出目录
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    # 1. 成绩分布直方图
    plt.figure(figsize=(10, 6))
    plt.hist(df['成绩'], bins=10, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title('学生成绩分布直方图')
    plt.xlabel('成绩')
    plt.ylabel('学生人数')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, '成绩分布直方图.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. 成绩等级饼图
    plt.figure(figsize=(10, 8))
    grade_counts = df['成绩等级'].value_counts()
    plt.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', 
            startangle=90, shadow=True, explode=[0.05] * len(grade_counts))
    plt.title('学生成绩等级分布')
    plt.axis('equal')
    plt.savefig(os.path.join(output_dir, '成绩等级分布.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. 成绩箱线图
    plt.figure(figsize=(8, 6))
    plt.boxplot(df['成绩'], patch_artist=True, 
                boxprops=dict(facecolor='lightblue', color='blue'),
                whiskerprops=dict(color='blue'),
                flierprops=dict(color='red', marker='o'))
    plt.title('学生成绩箱线图')
    plt.ylabel('成绩')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(output_dir, '成绩箱线图.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. 成绩条形图（按学生姓名排序）
    plt.figure(figsize=(12, 8))
    sorted_df = df.sort_values('成绩', ascending=False)
    bars = plt.bar(sorted_df['姓名'], sorted_df['成绩'], color='skyblue', edgecolor='black')
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.0f}', ha='center', va='bottom')
    
    plt.title('学生成绩条形图')
    plt.xlabel('学生姓名')
    plt.ylabel('成绩')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '学生成绩条形图.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"图表已保存到 '{output_dir}' 目录")

def export_results(df, stats, output_file='student_analysis_report.xlsx'):
    """
    导出分析结果到Excel文件
    
    参数:
        df (DataFrame): 包含学生成绩的DataFrame
        stats (dict): 包含统计信息的字典
        output_file (str): 输出文件名
    """
    # 创建Excel写入器
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # 1. 原始数据
        df.to_excel(writer, sheet_name='原始数据', index=False)
        
        # 2. 统计摘要
        summary_data = {
            '统计指标': [
                '学生人数', '成绩总和', '平均成绩', '中位成绩', 
                '最低成绩', '最高成绩', '标准差', '方差',
                '25%分位数', '75%分位数', '及格率(%)'
            ],
            '数值': [
                stats['count'], stats['total'], f"{stats['average']:.2f}", 
                f"{stats['median']:.2f}", stats['min'], stats['max'],
                f"{stats['std_dev']:.2f}", f"{stats['variance']:.2f}",
                f"{stats['percentile_25']:.2f}", f"{stats['percentile_75']:.2f}",
                f"{stats['passing_rate']:.2f}"
            ]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='统计摘要', index=False)
        
        # 3. 成绩分布
        grade_dist = pd.DataFrame({
            '成绩等级': list(stats['grade_distribution'].keys()),
            '学生人数': list(stats['grade_distribution'].values())
        })
        grade_dist.to_excel(writer, sheet_name='成绩分布', index=False)
        
        # 4. 学生排名
        ranking_df = df.sort_values('成绩', ascending=False)
        ranking_df['排名'] = range(1, len(ranking_df) + 1)
        ranking_df = ranking_df[['排名', '姓名', '成绩', '成绩等级']]
        ranking_df.to_excel(writer, sheet_name='学生排名', index=False)
    
    print(f"分析报告已导出到 '{output_file}'")

def display_results(filename):
    """
    显示分析结果
    
    参数:
        filename (str): 包含学生成绩的文件名
    """
    # 读取学生数据
    student_dict, df = read_student_data(filename)
    
    if student_dict is None or df is None:
        return
    
    # 计算统计信息
    stats = calculate_statistics(student_dict, df)
    
    if stats is None:
        return
    
    # 显示基本统计信息
    print(f"\n文件 '{filename}' 的分析结果:")
    print(f"学生人数: {stats['count']}")
    print(f"成绩总和: {stats['total']}")
    print(f"平均成绩: {stats['average']:.2f}")
    print(f"中位成绩: {stats['median']:.2f}")
    print(f"最低成绩: {stats['min']}")
    print(f"最高成绩: {stats['max']}")
    print(f"标准差: {stats['std_dev']:.2f}")
    print(f"方差: {stats['variance']:.2f}")
    print(f"25%分位数: {stats['percentile_25']:.2f}")
    print(f"75%分位数: {stats['percentile_75']:.2f}")
    print(f"及格率: {stats['passing_rate']:.2f}%")
    
    # 显示成绩分布
    print("\n成绩分布:")
    for grade, count in stats['grade_distribution'].items():
        print(f"{grade}: {count}人 ({count/stats['count']*100:.1f}%)")
    
    # 显示所有学生成绩
    print("\n学生成绩列表:")
    print("姓名\t成绩\t成绩等级\t与平均分的差距")
    print("-" * 50)
    for name, grade in student_dict.items():
        grade_level = df[df['姓名'] == name]['成绩等级'].values[0]
        diff = grade - stats['average']
        diff_str = f"+{diff:.2f}" if diff > 0 else f"{diff:.2f}"
        print(f"{name}\t{grade}\t{grade_level}\t{diff_str}")
    
    # 按成绩排序
    sorted_students = sorted(student_dict.items(), key=lambda x: x[1], reverse=True)
    
    print("\n成绩排名:")
    print("排名\t姓名\t成绩\t成绩等级")
    print("-" * 30)
    for i, (name, grade) in enumerate(sorted_students, 1):
        grade_level = df[df['姓名'] == name]['成绩等级'].values[0]
        print(f"{i}\t{name}\t{grade}\t{grade_level}")
    
    # 生成可视化图表
    generate_visualizations(df, stats)
    
    # 导出分析结果
    export_results(df, stats)

if __name__ == "__main__":
    # 默认文件名
    filename = "student_grades.csv"
    
    # 如果提供了命令行参数，使用它作为文件名
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    display_results(filename) 