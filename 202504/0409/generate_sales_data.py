import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sales_data(city, num_products=5, num_days=30):
    """生成销售数据"""
    # 产品类别
    product_categories = [
        '电子产品', '服装', '食品', '家居用品', '化妆品',
        '运动器材', '图书', '玩具', '办公用品', '珠宝首饰'
    ]
    
    # 随机选择产品类别
    selected_categories = np.random.choice(product_categories, num_products, replace=False)
    
    # 生成日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=num_days-1)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 生成销售数据
    data = []
    for date in dates:
        for category in selected_categories:
            # 生成随机销售额（1000-10000之间）
            sales = np.random.randint(1000, 10000)
            data.append({
                '日期': date,
                '产品类别': category,
                '销售额': sales
            })
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 按日期和产品类别排序
    df = df.sort_values(['日期', '产品类别'])
    
    return df

def main():
    # 设置随机种子以确保可重复性
    np.random.seed(42)
    
    # 生成北京销售数据
    beijing_data = generate_sales_data('北京')
    beijing_data.to_excel('sales_北京.xlsx', index=False)
    print("已生成北京销售数据：sales_北京.xlsx")
    
    # 生成上海销售数据
    shanghai_data = generate_sales_data('上海')
    shanghai_data.to_excel('sales_上海.xlsx', index=False)
    print("已生成上海销售数据：sales_上海.xlsx")
    
    # 显示数据示例
    print("\n北京销售数据示例：")
    print(beijing_data.head())
    print("\n上海销售数据示例：")
    print(shanghai_data.head())

if __name__ == "__main__":
    main() 