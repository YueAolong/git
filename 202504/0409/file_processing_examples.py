#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本展示了Python中各种文件处理和数据操作的示例。
包括文本文件、CSV文件、JSON文件的读写，以及数据结构的操作。
"""

import os
import csv
import json
import random
import string
import collections
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime

# ===== 1. 文本文件处理示例 =====

def create_sample_text_file(filename: str, num_lines: int = 10) -> None:
    """
    创建示例文本文件
    
    参数:
        filename (str): 文件名
        num_lines (int): 行数
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(num_lines):
            # 生成随机文本行
            line_length = random.randint(10, 50)
            random_text = ''.join(random.choice(string.ascii_letters + string.digits + ' ') 
                                for _ in range(line_length))
            f.write(f"行 {i+1}: {random_text}\n")
    
    print(f"已创建示例文本文件: {filename}")

def read_text_file_line_by_line(filename: str) -> List[str]:
    """
    逐行读取文本文件
    
    参数:
        filename (str): 文件名
        
    返回:
        List[str]: 文件行列表
    """
    lines = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                lines.append(line.strip())
        return lines
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return []

def process_text_file(filename: str) -> Dict[str, Any]:
    """
    处理文本文件，计算统计信息
    
    参数:
        filename (str): 文件名
        
    返回:
        Dict[str, Any]: 统计信息
    """
    lines = read_text_file_line_by_line(filename)
    if not lines:
        return {}
    
    # 计算统计信息
    stats = {
        '行数': len(lines),
        '总字符数': sum(len(line) for line in lines),
        '平均行长': sum(len(line) for line in lines) / len(lines) if lines else 0,
        '最长行': max(lines, key=len) if lines else "",
        '最短行': min(lines, key=len) if lines else "",
        '单词数': sum(len(line.split()) for line in lines)
    }
    
    return stats

# ===== 2. CSV文件处理示例 =====

def create_sample_csv_file(filename: str, num_rows: int = 10) -> None:
    """
    创建示例CSV文件
    
    参数:
        filename (str): 文件名
        num_rows (int): 行数
    """
    # 定义表头
    headers = ['ID', '姓名', '年龄', '城市', '工资']
    
    # 生成随机数据
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安']
    first_names = ['张', '王', '李', '赵', '刘', '陈', '杨', '黄', '周', '吴']
    last_names = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军']
    
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for i in range(num_rows):
            # 生成随机行数据
            row = [
                i + 1,  # ID
                random.choice(first_names) + random.choice(last_names),  # 姓名
                random.randint(18, 60),  # 年龄
                random.choice(cities),  # 城市
                random.randint(5000, 30000)  # 工资
            ]
            writer.writerow(row)
    
    print(f"已创建示例CSV文件: {filename}")

def read_csv_file(filename: str) -> Tuple[List[str], List[List[str]]]:
    """
    读取CSV文件
    
    参数:
        filename (str): 文件名
        
    返回:
        Tuple[List[str], List[List[str]]]: (表头, 数据行)
    """
    headers = []
    data = []
    
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            headers = next(reader)  # 读取表头
            for row in reader:
                data.append(row)
        return headers, data
    except Exception as e:
        print(f"读取CSV文件时发生错误: {e}")
        return [], []

def process_csv_file(filename: str) -> Dict[str, Any]:
    """
    处理CSV文件，计算统计信息
    
    参数:
        filename (str): 文件名
        
    返回:
        Dict[str, Any]: 统计信息
    """
    headers, data = read_csv_file(filename)
    if not headers or not data:
        return {}
    
    # 将数据转换为字典列表
    records = []
    for row in data:
        record = {}
        for i, value in enumerate(row):
            record[headers[i]] = value
        records.append(record)
    
    # 计算统计信息
    stats = {
        '行数': len(records),
        '列数': len(headers),
        '表头': headers
    }
    
    # 如果CSV包含数值列，计算统计量
    numeric_columns = []
    for header in headers:
        try:
            # 尝试将第一行转换为数值
            float(records[0][header])
            numeric_columns.append(header)
        except (ValueError, TypeError):
            pass
    
    # 计算数值列的统计量
    for column in numeric_columns:
        values = [float(record[column]) for record in records]
        stats[column] = {
            '总和': sum(values),
            '平均值': sum(values) / len(values),
            '最小值': min(values),
            '最大值': max(values)
        }
    
    # 计算分类列的统计量
    categorical_columns = [col for col in headers if col not in numeric_columns]
    for column in categorical_columns:
        values = [record[column] for record in records]
        counter = collections.Counter(values)
        stats[column] = {
            '唯一值数量': len(counter),
            '最常见的值': counter.most_common(1)[0][0] if counter else None,
            '值分布': dict(counter)
        }
    
    return stats

# ===== 3. JSON文件处理示例 =====

def create_sample_json_file(filename: str, num_items: int = 5) -> None:
    """
    创建示例JSON文件
    
    参数:
        filename (str): 文件名
        num_items (int): 项目数量
    """
    # 生成随机数据
    data = {
        '项目列表': [],
        '创建时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '版本': '1.0.0'
    }
    
    for i in range(num_items):
        item = {
            'ID': i + 1,
            '名称': f'项目 {i+1}',
            '描述': f'这是项目 {i+1} 的描述',
            '状态': random.choice(['进行中', '已完成', '已暂停']),
            '优先级': random.choice(['高', '中', '低']),
            '完成百分比': random.randint(0, 100),
            '标签': random.sample(['重要', '紧急', '常规', '长期'], random.randint(1, 3))
        }
        data['项目列表'].append(item)
    
    # 写入JSON文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"已创建示例JSON文件: {filename}")

def read_json_file(filename: str) -> Dict[str, Any]:
    """
    读取JSON文件
    
    参数:
        filename (str): 文件名
        
    返回:
        Dict[str, Any]: JSON数据
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"读取JSON文件时发生错误: {e}")
        return {}

def process_json_file(filename: str) -> Dict[str, Any]:
    """
    处理JSON文件，计算统计信息
    
    参数:
        filename (str): 文件名
        
    返回:
        Dict[str, Any]: 统计信息
    """
    data = read_json_file(filename)
    if not data:
        return {}
    
    # 计算统计信息
    stats = {
        '键数量': len(data),
        '键列表': list(data.keys())
    }
    
    # 如果包含项目列表，计算项目统计信息
    if '项目列表' in data and isinstance(data['项目列表'], list):
        projects = data['项目列表']
        stats['项目数量'] = len(projects)
        
        # 计算状态分布
        status_counts = collections.Counter(project['状态'] for project in projects)
        stats['状态分布'] = dict(status_counts)
        
        # 计算优先级分布
        priority_counts = collections.Counter(project['优先级'] for project in projects)
        stats['优先级分布'] = dict(priority_counts)
        
        # 计算完成百分比统计
        completion_percentages = [project['完成百分比'] for project in projects]
        stats['完成百分比'] = {
            '平均值': sum(completion_percentages) / len(completion_percentages),
            '最小值': min(completion_percentages),
            '最大值': max(completion_percentages)
        }
        
        # 统计标签
        all_tags = [tag for project in projects for tag in project.get('标签', [])]
        tag_counts = collections.Counter(all_tags)
        stats['标签统计'] = dict(tag_counts)
    
    return stats

# ===== 4. 文件操作综合示例 =====

def file_conversion_example() -> None:
    """
    文件格式转换示例：CSV转JSON
    """
    # 创建示例CSV文件
    csv_filename = 'example_data.csv'
    create_sample_csv_file(csv_filename, 5)
    
    # 读取CSV文件
    headers, data = read_csv_file(csv_filename)
    if not headers or not data:
        return
    
    # 转换为JSON格式
    json_data = {
        '表头': headers,
        '数据': []
    }
    
    for row in data:
        record = {}
        for i, value in enumerate(row):
            record[headers[i]] = value
        json_data['数据'].append(record)
    
    # 写入JSON文件
    json_filename = 'converted_data.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    
    print(f"已将CSV文件 '{csv_filename}' 转换为JSON文件 '{json_filename}'")

def data_filtering_example() -> None:
    """
    数据过滤示例：从CSV文件中筛选特定条件的数据
    """
    # 创建示例CSV文件
    csv_filename = 'employee_data.csv'
    create_sample_csv_file(csv_filename, 20)
    
    # 读取CSV文件
    headers, data = read_csv_file(csv_filename)
    if not headers or not data:
        return
    
    # 将数据转换为字典列表
    records = []
    for row in data:
        record = {}
        for i, value in enumerate(row):
            record[headers[i]] = value
        records.append(record)
    
    # 筛选条件：工资大于15000且年龄小于40的员工
    filtered_records = [
        record for record in records
        if float(record['工资']) > 15000 and int(record['年龄']) < 40
    ]
    
    # 将筛选结果写入新的CSV文件
    output_filename = 'high_salary_young_employees.csv'
    with open(output_filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for record in filtered_records:
            writer.writerow([record[header] for header in headers])
    
    print(f"已筛选出 {len(filtered_records)} 名高工资年轻员工，结果保存到 '{output_filename}'")

def data_aggregation_example() -> None:
    """
    数据聚合示例：按城市统计员工数量和平均工资
    """
    # 创建示例CSV文件
    csv_filename = 'company_data.csv'
    create_sample_csv_file(csv_filename, 30)
    
    # 读取CSV文件
    headers, data = read_csv_file(csv_filename)
    if not headers or not data:
        return
    
    # 将数据转换为字典列表
    records = []
    for row in data:
        record = {}
        for i, value in enumerate(row):
            record[headers[i]] = value
        records.append(record)
    
    # 按城市分组
    city_groups = collections.defaultdict(list)
    for record in records:
        city = record['城市']
        city_groups[city].append(record)
    
    # 计算每个城市的统计信息
    city_stats = {}
    for city, employees in city_groups.items():
        salaries = [float(emp['工资']) for emp in employees]
        city_stats[city] = {
            '员工数量': len(employees),
            '平均工资': sum(salaries) / len(salaries),
            '总工资': sum(salaries),
            '最高工资': max(salaries),
            '最低工资': min(salaries)
        }
    
    # 将统计结果写入JSON文件
    output_filename = 'city_statistics.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(city_stats, f, ensure_ascii=False, indent=4)
    
    print(f"已按城市统计员工数据，结果保存到 '{output_filename}'")
    
    # 显示统计结果
    print("\n城市统计结果:")
    for city, stats in city_stats.items():
        print(f"\n{city}:")
        print(f"  员工数量: {stats['员工数量']}")
        print(f"  平均工资: {stats['平均工资']:.2f}")
        print(f"  最高工资: {stats['最高工资']:.2f}")
        print(f"  最低工资: {stats['最低工资']:.2f}")

def main():
    """主函数"""
    print("===== Python文件处理和数据操作示例 =====\n")
    
    # 1. 文本文件处理示例
    print("1. 文本文件处理示例:")
    text_filename = 'sample_text.txt'
    create_sample_text_file(text_filename, 5)
    text_stats = process_text_file(text_filename)
    print(f"文本文件统计: {text_stats}\n")
    
    # 2. CSV文件处理示例
    print("2. CSV文件处理示例:")
    csv_filename = 'sample_data.csv'
    create_sample_csv_file(csv_filename, 8)
    csv_stats = process_csv_file(csv_filename)
    print(f"CSV文件统计: {csv_stats}\n")
    
    # 3. JSON文件处理示例
    print("3. JSON文件处理示例:")
    json_filename = 'sample_data.json'
    create_sample_json_file(json_filename, 4)
    json_stats = process_json_file(json_filename)
    print(f"JSON文件统计: {json_stats}\n")
    
    # 4. 文件操作综合示例
    print("4. 文件操作综合示例:")
    print("   a. 文件格式转换示例 (CSV转JSON):")
    file_conversion_example()
    print("\n   b. 数据过滤示例:")
    data_filtering_example()
    print("\n   c. 数据聚合示例:")
    data_aggregation_example()
    
    print("\n所有示例已完成!")

if __name__ == "__main__":
    main() 