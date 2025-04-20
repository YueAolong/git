#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
温度变化折线图绘制脚本
功能：
1. 生成随机温度数据
2. 使用matplotlib绘制温度随时间变化的折线图
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('TkAgg')  # 放在最上面


def generate_temperature_data(days: int = 30) -> pd.DataFrame:
    """
    生成随机温度数据

    参数:
        days (int): 生成数据的天数

    返回:
        pd.DataFrame: 包含日期和温度数据的DataFrame
    """
    # 生成日期序列
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(days)]

    # 生成随机温度数据
    np.random.seed(42)  # 设置随机种子，确保结果可重现

    # 基础温度（模拟春季温度）
    base_temp = 15

    # 添加周期性变化（模拟日温差）
    daily_variation = np.sin(np.linspace(0, 2 * np.pi * 3, days)) * 5

    # 添加上升趋势（模拟季节变化）
    trend = np.linspace(0, 5, days)

    # 添加随机波动
    random_variation = np.random.normal(0, 2, days)

    # 组合所有变化
    temperatures = base_temp + daily_variation + trend + random_variation

    # 创建DataFrame
    df = pd.DataFrame({
        '日期': dates,
        '温度': temperatures.round(1)
    })

    return df


def plot_temperature(df: pd.DataFrame, save_path: str = 'temperature_plot.png') -> None:
    """
    绘制温度变化折线图

    参数:
        df (pd.DataFrame): 包含日期和温度数据的DataFrame
        save_path (str): 图表保存路径
    """
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 创建图表
    plt.figure(figsize=(12, 6))

    # 绘制温度曲线
    plt.plot(df['日期'], df['温度'],
             marker='o',  # 数据点标记
             linestyle='-',  # 线型
             linewidth=2,  # 线宽
             color='#2E86C1',  # 线条颜色
             markersize=6,  # 标记大小
             label='实际温度')  # 图例标签

    # 添加平均温度线
    avg_temp = df['温度'].mean()
    plt.axhline(y=avg_temp,
                color='#E74C3C',  # 红色
                linestyle='--',  # 虚线
                label=f'平均温度: {avg_temp:.1f}°C')

    # 标记最高和最低温度点
    max_temp_idx = df['温度'].idxmax()
    min_temp_idx = df['温度'].idxmin()

    plt.plot(df['日期'][max_temp_idx], df['温度'][max_temp_idx],
             'r*',  # 红色星形
             markersize=15,
             label=f'最高温度: {df["温度"][max_temp_idx]:.1f}°C')

    plt.plot(df['日期'][min_temp_idx], df['温度'][min_temp_idx],
             'b*',  # 蓝色星形
             markersize=15,
             label=f'最低温度: {df["温度"][min_temp_idx]:.1f}°C')

    # 设置图表标题和轴标签
    plt.title('每日温度变化趋势', fontsize=16, pad=15)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('温度 (°C)', fontsize=12)

    # 设置网格
    plt.grid(True, linestyle='--', alpha=0.7)

    # 自动调整x轴日期标签
    plt.gcf().autofmt_xdate()

    # 添加图例
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # 调整布局，确保所有元素都能显示
    plt.tight_layout()

    # 保存图表
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\n温度变化图表已保存为: {save_path}")

    # 显示图表
    plt.show()


def main():
    """主函数"""
    print("===== 温度变化折线图生成程序 =====")

    # 获取用户输入的天数
    while True:
        try:
            days = int(input("请输入要生成的天数 (默认30天): ") or "30")
            if days > 0:
                break
            else:
                print("请输入大于0的天数")
        except ValueError:
            print("请输入有效的数字")

    # 生成数据
    print(f"\n生成{days}天的随机温度数据...")
    df = generate_temperature_data(days)

    # 显示数据概要
    print("\n数据概要:")
    print(f"数据范围: {df['日期'].min().strftime('%Y-%m-%d')} 到 {df['日期'].max().strftime('%Y-%m-%d')}")
    print(f"温度范围: {df['温度'].min():.1f}°C 到 {df['温度'].max():.1f}°C")
    print(f"平均温度: {df['温度'].mean():.1f}°C")

    # 绘制图表
    print("\n正在生成温度变化折线图...")
    plot_temperature(df)

    # 保存数据到CSV文件
    df.to_csv('temperature_data.csv', index=False, encoding='utf-8-sig')
    print("\n温度数据已保存为: temperature_data.csv")


if __name__ == "__main__":
    main()
