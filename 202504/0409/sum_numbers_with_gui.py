#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本使用图形界面弹窗让用户选择文件，然后读取文件内容，提取文件中的数字，并计算这些数字的总和。
"""

import re
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk

class NumberSumCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("文件数字总和计算器")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10))
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建文件选择部分
        self.create_file_selection_frame()
        
        # 创建结果显示部分
        self.create_results_frame()
        
        # 创建按钮部分
        self.create_buttons_frame()
        
        # 初始化变量
        self.selected_file = None
        self.numbers = []
        self.total_sum = 0
        self.line_sums = {}
    
    def create_file_selection_frame(self):
        """创建文件选择部分"""
        file_frame = ttk.LabelFrame(self.main_frame, text="文件选择", padding="5")
        file_frame.pack(fill=tk.X, pady=5)
        
        # 文件路径显示
        self.file_path_var = tk.StringVar()
        self.file_path_var.set("未选择文件")
        
        file_path_label = ttk.Label(file_frame, textvariable=self.file_path_var, wraplength=600)
        file_path_label.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        # 浏览按钮
        browse_button = ttk.Button(file_frame, text="浏览...", command=self.browse_file)
        browse_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def create_results_frame(self):
        """创建结果显示部分"""
        results_frame = ttk.LabelFrame(self.main_frame, text="计算结果", padding="5")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建选项卡
        tab_control = ttk.Notebook(results_frame)
        
        # 总体结果选项卡
        overall_tab = ttk.Frame(tab_control)
        tab_control.add(overall_tab, text="总体结果")
        
        # 总体结果文本框
        self.overall_text = scrolledtext.ScrolledText(overall_tab, wrap=tk.WORD, height=10)
        self.overall_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 按行结果选项卡
        line_tab = ttk.Frame(tab_control)
        tab_control.add(line_tab, text="按行结果")
        
        # 按行结果文本框
        self.line_text = scrolledtext.ScrolledText(line_tab, wrap=tk.WORD, height=10)
        self.line_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 文件内容选项卡
        content_tab = ttk.Frame(tab_control)
        tab_control.add(content_tab, text="文件内容")
        
        # 文件内容文本框
        self.content_text = scrolledtext.ScrolledText(content_tab, wrap=tk.WORD, height=10)
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tab_control.pack(fill=tk.BOTH, expand=True)
    
    def create_buttons_frame(self):
        """创建按钮部分"""
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        
        # 计算按钮
        calculate_button = ttk.Button(buttons_frame, text="计算总和", command=self.calculate_sum)
        calculate_button.pack(side=tk.LEFT, padx=5)
        
        # 清除按钮
        clear_button = ttk.Button(buttons_frame, text="清除结果", command=self.clear_results)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 退出按钮
        exit_button = ttk.Button(buttons_frame, text="退出", command=self.root.quit)
        exit_button.pack(side=tk.RIGHT, padx=5)
    
    def browse_file(self):
        """打开文件选择对话框"""
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_path_var.set(file_path)
            
            # 显示文件内容
            self.display_file_content()
    
    def display_file_content(self):
        """显示文件内容"""
        if not self.selected_file or not os.path.exists(self.selected_file):
            return
        
        try:
            with open(self.selected_file, 'r', encoding='utf-8') as file:
                content = file.read()
                self.content_text.delete(1.0, tk.END)
                self.content_text.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("错误", f"读取文件时发生错误: {e}")
    
    def calculate_sum_from_file(self):
        """读取文件内容，提取数字并计算总和"""
        if not self.selected_file or not os.path.exists(self.selected_file):
            messagebox.showerror("错误", "请先选择一个有效的文件!")
            return 0, []
        
        numbers = []
        total_sum = 0
        
        try:
            with open(self.selected_file, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # 使用正则表达式提取所有数字（包括整数、小数、负数和科学计数法）
                number_pattern = r'-?\d+\.?\d*e?[+-]?\d*'
                found_numbers = re.findall(number_pattern, content)
                
                # 将提取的字符串转换为浮点数
                for num_str in found_numbers:
                    try:
                        num = float(num_str)
                        numbers.append(num)
                        total_sum += num
                    except ValueError:
                        print(f"警告: 无法将 '{num_str}' 转换为数字，已跳过")
            
            return total_sum, numbers
        
        except Exception as e:
            messagebox.showerror("错误", f"读取文件时发生错误: {e}")
            return 0, []
    
    def calculate_sum_by_line(self):
        """按行读取文件，提取每行中的数字并计算总和"""
        if not self.selected_file or not os.path.exists(self.selected_file):
            return {}
        
        line_sums = {}
        
        try:
            with open(self.selected_file, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    # 使用正则表达式提取当前行中的所有数字
                    number_pattern = r'-?\d+\.?\d*e?[+-]?\d*'
                    found_numbers = re.findall(number_pattern, line)
                    
                    # 将提取的字符串转换为浮点数
                    line_numbers = []
                    line_sum = 0
                    
                    for num_str in found_numbers:
                        try:
                            num = float(num_str)
                            line_numbers.append(num)
                            line_sum += num
                        except ValueError:
                            print(f"警告: 第 {line_num} 行中无法将 '{num_str}' 转换为数字，已跳过")
                    
                    # 存储当前行的数字和总和
                    line_sums[line_num] = {
                        'numbers': line_numbers,
                        'sum': line_sum
                    }
            
            return line_sums
        
        except Exception as e:
            messagebox.showerror("错误", f"读取文件时发生错误: {e}")
            return {}
    
    def calculate_sum(self):
        """计算文件中数字的总和"""
        if not self.selected_file:
            messagebox.showwarning("警告", "请先选择一个文件!")
            return
        
        # 计算文件中所有数字的总和
        self.total_sum, self.numbers = self.calculate_sum_from_file()
        
        # 按行计算数字总和
        self.line_sums = self.calculate_sum_by_line()
        
        # 计算所有行的总和
        total_line_sum = sum(line_info['sum'] for line_info in self.line_sums.values())
        
        # 显示总体结果
        self.overall_text.delete(1.0, tk.END)
        self.overall_text.insert(tk.END, f"文件: {self.selected_file}\n\n")
        self.overall_text.insert(tk.END, f"从文件中提取了 {len(self.numbers)} 个数字\n")
        self.overall_text.insert(tk.END, f"数字列表: {self.numbers}\n")
        self.overall_text.insert(tk.END, f"数字总和: {self.total_sum}\n\n")
        self.overall_text.insert(tk.END, f"所有行的数字总和: {total_line_sum}\n\n")
        
        # 验证两种方法计算的总和是否一致
        if abs(self.total_sum - total_line_sum) < 1e-10:  # 考虑浮点数精度
            self.overall_text.insert(tk.END, "验证成功: 两种方法计算的总和一致!\n")
        else:
            self.overall_text.insert(tk.END, f"警告: 两种方法计算的总和不一致! 方法1: {self.total_sum}, 方法2: {total_line_sum}\n")
        
        # 显示按行结果
        self.line_text.delete(1.0, tk.END)
        self.line_text.insert(tk.END, f"文件: {self.selected_file}\n\n")
        self.line_text.insert(tk.END, "按行统计结果:\n\n")
        
        for line_num, line_info in self.line_sums.items():
            self.line_text.insert(tk.END, f"第 {line_num} 行: 数字 {line_info['numbers']}, 总和 {line_info['sum']}\n")
    
    def clear_results(self):
        """清除结果"""
        self.overall_text.delete(1.0, tk.END)
        self.line_text.delete(1.0, tk.END)
        self.numbers = []
        self.total_sum = 0
        self.line_sums = {}

def main():
    """主函数"""
    root = tk.Tk()
    app = NumberSumCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 