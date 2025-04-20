import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# 设置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

class ExcelProcessor:
    def __init__(self):
        self.df = None
        self.file_path = None
        
    def select_file(self):
        """选择Excel文件"""
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            self.file_path = file_path
            return True
        return False
    
    def read_excel(self):
        """读取Excel文件"""
        try:
            self.df = pd.read_excel(self.file_path, header=0)  # 第一行作为列名
            return True
        except Exception as e:
            messagebox.showerror("错误", f"读取Excel文件时出错：{str(e)}")
            return False
    
    def calculate_averages(self):
        """计算每一列的平均值"""
        try:
            averages = self.df.mean()
            return averages
        except Exception as e:
            messagebox.showerror("错误", f"计算平均值时出错：{str(e)}")
            return None
    
    def plot_bar_chart(self, averages):
        """绘制柱状图"""
        try:
            # 创建图形
            plt.figure(figsize=(12, 6))
            
            # 绘制柱状图
            bars = plt.bar(range(len(averages)), averages.values)
            
            # 设置标题和标签
            plt.title('各列数据平均值', fontsize=14, pad=20)
            plt.xlabel('列名', fontsize=12)
            plt.ylabel('平均值', fontsize=12)
            
            # 设置x轴刻度标签
            plt.xticks(range(len(averages)), averages.index, rotation=45, ha='right')
            
            # 在柱子上添加数值标签
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}',
                        ha='center', va='bottom')
            
            # 调整布局
            plt.tight_layout()
            
            # 保存图片
            output_path = os.path.join(os.path.dirname(self.file_path), 'averages_bar_chart.png')
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            messagebox.showinfo("成功", f"柱状图已保存至：{output_path}")
            return True
        except Exception as e:
            messagebox.showerror("错误", f"绘制图表时出错：{str(e)}")
            return False

def main():
    processor = ExcelProcessor()
    
    # 选择Excel文件
    if not processor.select_file():
        print("未选择文件，程序退出")
        return
    
    # 读取Excel文件
    if not processor.read_excel():
        return
    
    # 计算每一列的平均值
    averages = processor.calculate_averages()
    if averages is not None:
        print("\n各列平均值：")
        for col, avg in averages.items():
            print(f"{col}：{avg:.2f}")
        
        # 绘制柱状图
        processor.plot_bar_chart(averages)

if __name__ == "__main__":
    main() 