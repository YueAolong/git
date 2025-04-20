import pandas as pd
import numpy as np

# 创建测试数据
data = {
    '姓名': ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十'],
    '年龄': [25, 30, 35, 28, 32, 27, 33, 29],
    '部门': ['技术部', '市场部', '人事部', '技术部', '财务部', '市场部', '技术部', '人事部']
}

# 创建DataFrame
df = pd.DataFrame(data)

# 显示DataFrame
print("测试数据：")
print(df)

# 显示基本统计信息
print("\n基本统计信息：")
print(df.describe())

# 显示各部门人数
print("\n各部门人数：")
print(df['部门'].value_counts()) 