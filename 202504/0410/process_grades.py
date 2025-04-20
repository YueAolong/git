#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本用于处理成绩列表，包括：
1. 打印原始成绩列表
2. 去重
3. 排序
4. 计算平均值
5. 筛选高于80分的成绩
"""


def process_grades(grades: list) -> None:
    """
    处理成绩列表
    
    参数:
        grades (list): 成绩列表
    """
    # 1. 打印原始成绩列表
    print("\n原始成绩列表:")
    print(grades)
    
    # 2. 去重
    unique_grades = list(set(grades))
    print("\n去重后的成绩列表:")
    print(unique_grades)
    
    # 3. 排序
    sorted_grades = sorted(unique_grades)
    print("\n排序后的成绩列表:")
    print(sorted_grades)
    
    # 4. 计算平均值
    average = sum(grades) / len(grades)
    print(f"\n成绩平均值: {average:.2f}")
    
    # 5. 筛选高于80分的成绩
    high_grades = [grade for grade in grades if grade > 80]
    print("\n高于80分的成绩:")
    print(high_grades)


def main():
    """主函数"""
    # 示例成绩列表
    grades = [85, 92, 78, 90, 88, 85, 92, 95, 88, 90]
    
    print("===== 成绩处理程序 =====")
    process_grades(grades)


if __name__ == "__main__":
    main()
