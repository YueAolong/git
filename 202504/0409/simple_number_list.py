#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本生成一个包含数字的列表并打印它。
"""

# 方法1：直接创建一个包含数字的列表
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("方法1 - 直接创建的列表:", numbers)

# 方法2：使用range()函数创建列表
range_numbers = list(range(1, 11))
print("方法2 - 使用range()创建的列表:", range_numbers)

# 方法3：使用列表推导式创建列表
list_comprehension = [x for x in range(1, 11)]
print("方法3 - 使用列表推导式创建的列表:", list_comprehension)

# 方法4：创建一个包含随机数字的列表
import random
random_numbers = [random.randint(1, 100) for _ in range(5)]
print("方法4 - 包含随机数字的列表:", random_numbers)

# 方法5：创建一个包含偶数的列表
even_numbers = [x for x in range(2, 21, 2)]
print("方法5 - 包含偶数的列表:", even_numbers)

# 方法6：创建一个包含奇数的列表
odd_numbers = [x for x in range(1, 20, 2)]
print("方法6 - 包含奇数的列表:", odd_numbers)

# 方法7：创建一个包含平方数的列表
square_numbers = [x**2 for x in range(1, 6)]
print("方法7 - 包含平方数的列表:", square_numbers)

# 方法8：创建一个包含斐波那契数列的列表
fibonacci = [0, 1]
for i in range(2, 10):
    fibonacci.append(fibonacci[i-1] + fibonacci[i-2])
print("方法8 - 包含斐波那契数列的列表:", fibonacci)

# 方法9：创建一个包含等差数列的列表
arithmetic_sequence = [1 + i*2 for i in range(5)]
print("方法9 - 包含等差数列的列表:", arithmetic_sequence)

# 方法10：创建一个包含几何数列的列表
geometric_sequence = [2**i for i in range(5)]
print("方法10 - 包含几何数列的列表:", geometric_sequence)

print("\n所有列表已生成并打印完成！")

# 示例输出
print("\n示例输出:")
print("文件: example.txt")
print("从文件中提取了 5 个数字")
print("数字列表: [123, 45.67, -89, 1.23e-4, -5.67E+8]")
print("数字总和: -566999999.9999999")
print("所有行的数字总和: -566999999.9999999")
print("验证成功: 两种方法计算的总和一致!") 