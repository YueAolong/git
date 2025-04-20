#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图形化数据清洗脚本（适配 EXE）
"""

import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from typing import Optional


def select_file() -> Optional[str]:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="选择CSV文件",
        filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
    )
    return file_path if file_path else None


def generate_sample_data(output_file: str = 'sample_data.csv') -> str:
    np.random.seed(42)
    data = {
        'ID': list(range(1, 21)),
        '姓名': [f'用户{i}' for i in range(1, 21)],
        '年龄': np.random.randint(18, 60, size=20).astype(float),  # 使用float，支持NaN
        '工资': np.random.randint(5000, 20000, size=20).astype(float),
        '评分': np.random.uniform(1, 10, size=20).round(1).astype(object)
    }

    df = pd.DataFrame(data)

    # 插入空值
    df.at[5, '年龄'] = np.nan
    df.at[10, '工资'] = np.nan
    df.at[15, '评分'] = np.nan

    # 添加重复行
    df.loc[18] = df.loc[4]
    df.loc[18, 'ID'] = 5
    df.loc[18, '姓名'] = '用户5'

    # 插入非数值评分
    df.at[3, '评分'] = 'N/A'
    df.at[7, '评分'] = '未知'

    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    messagebox.showinfo("完成", f"示例数据已生成: {output_file}")
    return output_file


def clean_data(file_path: str, float_column: str = '评分') -> None:
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='gbk')

    # 删除空值
    df_cleaned = df.dropna()

    # 删除重复数据
    df_cleaned = df_cleaned.drop_duplicates()

    # 尝试转换为浮点数
    if float_column in df_cleaned.columns:
        df_cleaned[float_column] = pd.to_numeric(df_cleaned[float_column], errors='coerce')
        df_cleaned = df_cleaned.dropna(subset=[float_column])

    output_file = os.path.splitext(file_path)[0] + '_cleaned.csv'
    try:
        df_cleaned.to_csv(output_file, index=False, encoding='utf-8-sig')
        messagebox.showinfo("完成", f"清洗后的文件已保存为：\n{output_file}")
    except PermissionError:
        messagebox.showerror("错误", f"无法写入文件，请关闭文件后重试：\n{output_file}")


def main():
    root = tk.Tk()
    root.withdraw()

    # 提问是否生成示例数据
    use_sample = messagebox.askyesno("选择数据", "是否生成示例数据？\n是：生成示例数据\n否：选择已有CSV文件")
    if use_sample:
        file_path = generate_sample_data()
    else:
        file_path = select_file()
        if not file_path:
            messagebox.showwarning("未选择文件", "未选择CSV文件，程序退出")
            return

    # 让用户输入需要转换的列名
    float_column = simpledialog.askstring("列名输入", "请输入要转换为浮点数的列名：", initialvalue="评分")
    if not float_column:
        float_column = "评分"

    clean_data(file_path, float_column)


if __name__ == "__main__":
    main()
