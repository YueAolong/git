#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本创建一个包含姓名和分数的DataFrame，并计算平均分。
"""

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from typing import List, Dict, Any


def generate_sample_data(num_students: int = 10, min_score: int = 60, max_score: int = 100) -> pd.DataFrame:
    """
    生成示例学生成绩数据
    
    参数:
        num_students (int): 学生数量
        min_score (int): 最低分数
        max_score (int): 最高分数
        
    返回:
        pd.DataFrame: 包含姓名和分数的DataFrame
    """
    # 生成随机中文姓名
    first_names = ['张', '王', '李', '赵', '刘', '陈', '杨', '黄', '周', '吴']
    last_names = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军']
    
    names = [random.choice(first_names) + random.choice(last_names) for _ in range(num_students)]
    
    # 生成随机分数
    scores = [random.randint(min_score, max_score) for _ in range(num_students)]
    
    # 创建DataFrame
    df = pd.DataFrame({
        '姓名': names,
        '分数': scores
    })
    
    return df


def calculate_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    计算成绩统计信息
    
    参数:
        df (pd.DataFrame): 包含姓名和分数的DataFrame
        
    返回:
        Dict[str, Any]: 统计信息
    """
    stats = {
        '平均分': df['分数'].mean(),
        '最高分': df['分数'].max(),
        '最低分': df['分数'].min(),
        '中位数': df['分数'].median(),
        '标准差': df['分数'].std(),
        '及格率': (df['分数'] >= 60).mean() * 100,
        '优秀率': (df['分数'] >= 90).mean() * 100
    }
    
    return stats


def display_results(df: pd.DataFrame, stats: Dict[str, Any]) -> None:
    """
    显示结果
    
    参数:
        df (pd.DataFrame): 包含姓名和分数的DataFrame
        stats (Dict[str, Any]): 统计信息
    """
    print("\n===== 学生成绩数据 =====")
    print(df)
    
    print("\n===== 成绩统计 =====")
    for key, value in stats.items():
        if '率' in key:
            print(f"{key}: {value:.2f}%")
        else:
            print(f"{key}: {value:.2f}")
    
    # 按分数排序
    sorted_df = df.sort_values(by='分数', ascending=False)
    print("\n===== 成绩排名 =====")
    print(sorted_df)


def visualize_data(df: pd.DataFrame) -> None:
    """
    可视化数据
    
    参数:
        df (pd.DataFrame): 包含姓名和分数的DataFrame
    """
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 柱状图
    ax1.bar(df['姓名'], df['分数'], color='skyblue')
    ax1.set_title('学生成绩柱状图')
    ax1.set_xlabel('姓名')
    ax1.set_ylabel('分数')
    ax1.set_ylim(0, 100)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 箱线图
    ax2.boxplot(df['分数'], labels=['分数'])
    ax2.set_title('分数箱线图')
    ax2.set_ylabel('分数')
    
    plt.tight_layout()
    plt.savefig('score_visualization.png')
    print("\n图表已保存为 'score_visualization.png'")


def main():
    """主函数"""
    print("===== 学生成绩分析程序 =====")
    
    # 生成示例数据
    num_students = int(input("请输入学生数量 (默认10): ") or "10")
    df = generate_sample_data(num_students)
    
    # 计算统计信息
    stats = calculate_statistics(df)
    
    # 显示结果
    display_results(df, stats)
    
    # 可视化数据
    try:
        visualize_data(df)
    except Exception as e:
        print(f"可视化数据时发生错误: {e}")
        print("跳过可视化步骤")


if __name__ == "__main__":
    main() 