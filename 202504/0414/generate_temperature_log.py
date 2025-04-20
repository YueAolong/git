#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
温度日志生成脚本
功能：
1. 生成30天的温度日志数据
2. 包含日期和两个传感器的温度读数
3. 保存为CSV文件
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_temperature_log(days: int = 30, output_file: str = 'temperature_log.csv') -> str:
    """
    生成温度日志数据并保存为CSV文件
    
    参数:
        days (int): 生成数据的天数
        output_file (str): 输出文件名
        
    返回:
        str: 生成的文件路径
    """
    # 生成日期序列
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    # 生成随机温度数据
    np.random.seed(42)  # 设置随机种子，确保结果可重现
    
    # 基础温度（模拟春季温度）
    base_temp = 15
    
    # 添加周期性变化（模拟日温差）
    daily_variation = np.sin(np.linspace(0, 2*np.pi*3, days)) * 5
    
    # 添加上升趋势（模拟季节变化）
    trend = np.linspace(0, 5, days)
    
    # 添加随机波动
    random_variation1 = np.random.normal(0, 2, days)
    random_variation2 = np.random.normal(0, 2, days)
    
    # 组合所有变化
    temperatures1 = base_temp + daily_variation + trend + random_variation1
    temperatures2 = base_temp + daily_variation + trend + random_variation2 + np.random.normal(0, 1, days)  # 第二个传感器有额外波动
    
    # 创建DataFrame
    df = pd.DataFrame({
        '日期': dates,
        '传感器1温度': temperatures1.round(1),
        '传感器2温度': temperatures2.round(1)
    })
    
    # 保存为CSV文件
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"已生成温度日志文件: {output_file}")
    
    # 显示数据概要
    print("\n数据概要:")
    print(f"数据范围: {df['日期'].min().strftime('%Y-%m-%d')} 到 {df['日期'].max().strftime('%Y-%m-%d')}")
    print(f"传感器1温度范围: {df['传感器1温度'].min():.1f}°C 到 {df['传感器1温度'].max():.1f}°C")
    print(f"传感器2温度范围: {df['传感器2温度'].min():.1f}°C 到 {df['传感器2温度'].max():.1f}°C")
    print(f"传感器1平均温度: {df['传感器1温度'].mean():.1f}°C")
    print(f"传感器2平均温度: {df['传感器2温度'].mean():.1f}°C")
    
    return output_file

def main():
    """主函数"""
    print("===== 温度日志生成程序 =====")
    
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
    print(f"\n生成{days}天的温度日志数据...")
    generate_temperature_log(days)
    
    print("\n温度日志数据已生成完成！")

if __name__ == "__main__":
    main() 