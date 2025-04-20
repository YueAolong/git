#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本演示了Python中数据结构和文件处理的结合使用。
它读取学生成绩数据，将数据存储到不同的数据结构中，并进行多种分析。
"""

import os
import csv
import json
import statistics
import collections
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any, Optional

class StudentDataAnalyzer:
    """学生数据分析器类，用于处理和分析学生成绩数据"""
    
    def __init__(self, filename: str):
        """
        初始化分析器
        
        参数:
            filename (str): 包含学生成绩的CSV文件名
        """
        self.filename = filename
        self.students_dict = {}  # 字典格式: {学生姓名: 成绩}
        self.students_list = []  # 列表格式: [{'姓名': 姓名, '成绩': 成绩}, ...]
        self.grades_by_level = collections.defaultdict(list)  # 按成绩等级分组
        self.df = None  # pandas DataFrame格式
        
        # 成绩等级定义
        self.grade_levels = {
            '优秀': (90, 100),
            '良好': (80, 89),
            '中等': (70, 79),
            '及格': (60, 69),
            '不及格': (0, 59)
        }
    
    def load_data(self) -> bool:
        """
        从CSV文件加载学生数据到不同的数据结构中
        
        返回:
            bool: 数据加载是否成功
        """
        if not os.path.exists(self.filename):
            print(f"错误: 文件 '{self.filename}' 不存在!")
            return False
        
        try:
            # 1. 使用pandas读取CSV文件
            self.df = pd.read_csv(self.filename, encoding='utf-8-sig')
            
            # 2. 将数据加载到字典中
            for _, row in self.df.iterrows():
                name = row['姓名']
                grade = row['成绩']
                self.students_dict[name] = grade
                
                # 3. 将数据加载到列表中
                self.students_list.append({
                    '姓名': name,
                    '成绩': grade
                })
                
                # 4. 按成绩等级分组
                level = self._get_grade_level(grade)
                self.grades_by_level[level].append(name)
            
            print(f"成功加载了 {len(self.students_dict)} 名学生的数据")
            return True
            
        except Exception as e:
            print(f"错误: 读取文件时发生错误: {e}")
            return False
    
    def _get_grade_level(self, grade: float) -> str:
        """
        根据成绩确定等级
        
        参数:
            grade (float): 学生成绩
            
        返回:
            str: 成绩等级
        """
        for level, (min_grade, max_grade) in self.grade_levels.items():
            if min_grade <= grade <= max_grade:
                return level
        return "未知"
    
    def calculate_basic_stats(self) -> Dict[str, Any]:
        """
        计算基本统计信息
        
        返回:
            Dict[str, Any]: 包含统计信息的字典
        """
        if not self.students_dict:
            return {}
        
        grades = list(self.students_dict.values())
        
        stats = {
            'count': len(self.students_dict),
            'total': sum(grades),
            'average': statistics.mean(grades),
            'median': statistics.median(grades),
            'min': min(grades),
            'max': max(grades),
            'std_dev': statistics.stdev(grades) if len(grades) > 1 else 0,
            'variance': statistics.variance(grades) if len(grades) > 1 else 0
        }
        
        # 计算百分位数
        if len(grades) >= 4:
            stats['percentile_25'] = statistics.quantiles(grades, n=4)[0]
            stats['percentile_75'] = statistics.quantiles(grades, n=4)[2]
        
        # 计算及格率
        passing_count = sum(1 for grade in grades if grade >= 60)
        stats['passing_rate'] = passing_count / len(grades) * 100
        
        return stats
    
    def find_top_students(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        找出成绩最高的n名学生
        
        参数:
            n (int): 返回的学生数量
            
        返回:
            List[Dict[str, Any]]: 包含学生信息的列表
        """
        if not self.students_dict:
            return []
        
        # 按成绩排序
        sorted_students = sorted(self.students_dict.items(), key=lambda x: x[1], reverse=True)
        
        # 返回前n名
        return [{'姓名': name, '成绩': grade, '排名': i+1} 
                for i, (name, grade) in enumerate(sorted_students[:n])]
    
    def find_students_by_level(self, level: str) -> List[Dict[str, Any]]:
        """
        找出指定等级的所有学生
        
        参数:
            level (str): 成绩等级
            
        返回:
            List[Dict[str, Any]]: 包含学生信息的列表
        """
        if level not in self.grades_by_level:
            return []
        
        students = self.grades_by_level[level]
        return [{'姓名': name, '成绩': self.students_dict[name]} for name in students]
    
    def generate_grade_distribution(self) -> Dict[str, int]:
        """
        生成成绩分布统计
        
        返回:
            Dict[str, int]: 各等级的学生人数
        """
        distribution = {}
        for level in self.grade_levels.keys():
            distribution[level] = len(self.grades_by_level[level])
        return distribution
    
    def export_to_json(self, output_file: str = 'student_analysis.json') -> bool:
        """
        将分析结果导出为JSON文件
        
        参数:
            output_file (str): 输出文件名
            
        返回:
            bool: 导出是否成功
        """
        try:
            # 收集所有分析结果
            results = {
                '基本信息': {
                    '学生总数': len(self.students_dict),
                    '分析时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                '统计信息': self.calculate_basic_stats(),
                '成绩分布': self.generate_grade_distribution(),
                '前5名学生': self.find_top_students(5),
                '各等级学生': {level: self.find_students_by_level(level) 
                           for level in self.grade_levels.keys()}
            }
            
            # 写入JSON文件
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            
            print(f"分析结果已导出到 '{output_file}'")
            return True
            
        except Exception as e:
            print(f"错误: 导出JSON文件时发生错误: {e}")
            return False
    
    def export_to_csv(self, output_file: str = 'student_analysis.csv') -> bool:
        """
        将学生数据导出为CSV文件，包含排名和等级信息
        
        参数:
            output_file (str): 输出文件名
            
        返回:
            bool: 导出是否成功
        """
        try:
            if self.df is None:
                return False
            
            # 添加排名和等级列
            result_df = self.df.copy()
            result_df['排名'] = result_df['成绩'].rank(ascending=False, method='min').astype(int)
            result_df['成绩等级'] = result_df['成绩'].apply(self._get_grade_level)
            
            # 按排名排序
            result_df = result_df.sort_values('排名')
            
            # 导出到CSV
            result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            
            print(f"学生数据已导出到 '{output_file}'")
            return True
            
        except Exception as e:
            print(f"错误: 导出CSV文件时发生错误: {e}")
            return False
    
    def generate_charts(self, output_dir: str = 'charts') -> bool:
        """
        生成可视化图表
        
        参数:
            output_dir (str): 图表输出目录
            
        返回:
            bool: 生成是否成功
        """
        if self.df is None:
            return False
        
        try:
            # 创建输出目录
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
            plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
            
            # 1. 成绩分布直方图
            plt.figure(figsize=(10, 6))
            plt.hist(self.df['成绩'], bins=10, alpha=0.7, color='skyblue', edgecolor='black')
            plt.title('学生成绩分布直方图')
            plt.xlabel('成绩')
            plt.ylabel('学生人数')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.savefig(os.path.join(output_dir, '成绩分布直方图.png'), dpi=300, bbox_inches='tight')
            plt.close()
            
            # 2. 成绩等级饼图
            plt.figure(figsize=(10, 8))
            grade_counts = self.df['成绩'].apply(self._get_grade_level).value_counts()
            plt.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', 
                    startangle=90, shadow=True, explode=[0.05] * len(grade_counts))
            plt.title('学生成绩等级分布')
            plt.axis('equal')
            plt.savefig(os.path.join(output_dir, '成绩等级分布.png'), dpi=300, bbox_inches='tight')
            plt.close()
            
            # 3. 成绩条形图（按学生姓名排序）
            plt.figure(figsize=(12, 8))
            sorted_df = self.df.sort_values('成绩', ascending=False)
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
            return True
            
        except Exception as e:
            print(f"错误: 生成图表时发生错误: {e}")
            return False
    
    def display_summary(self) -> None:
        """显示分析摘要"""
        if not self.students_dict:
            print("没有数据可供分析")
            return
        
        # 计算统计信息
        stats = self.calculate_basic_stats()
        
        # 显示基本统计信息
        print(f"\n文件 '{self.filename}' 的分析结果:")
        print(f"学生人数: {stats['count']}")
        print(f"成绩总和: {stats['total']}")
        print(f"平均成绩: {stats['average']:.2f}")
        print(f"中位成绩: {stats['median']:.2f}")
        print(f"最低成绩: {stats['min']}")
        print(f"最高成绩: {stats['max']}")
        print(f"标准差: {stats['std_dev']:.2f}")
        print(f"方差: {stats['variance']:.2f}")
        
        if 'percentile_25' in stats:
            print(f"25%分位数: {stats['percentile_25']:.2f}")
            print(f"75%分位数: {stats['percentile_75']:.2f}")
        
        print(f"及格率: {stats['passing_rate']:.2f}%")
        
        # 显示成绩分布
        distribution = self.generate_grade_distribution()
        print("\n成绩分布:")
        for level, count in distribution.items():
            print(f"{level}: {count}人 ({count/stats['count']*100:.1f}%)")
        
        # 显示前5名学生
        top_students = self.find_top_students(5)
        print("\n前5名学生:")
        print("排名\t姓名\t成绩")
        print("-" * 20)
        for student in top_students:
            print(f"{student['排名']}\t{student['姓名']}\t{student['成绩']}")
    
    def run_full_analysis(self) -> None:
        """
        运行完整的分析流程
        """
        # 1. 加载数据
        if not self.load_data():
            return
        
        # 2. 显示摘要
        self.display_summary()
        
        # 3. 导出结果
        self.export_to_json()
        self.export_to_csv()
        
        # 4. 生成图表
        self.generate_charts()


def main():
    """主函数"""
    # 默认文件名
    filename = "student_grades.csv"
    
    # 如果提供了命令行参数，使用它作为文件名
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    # 创建分析器并运行分析
    analyzer = StudentDataAnalyzer(filename)
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main() 