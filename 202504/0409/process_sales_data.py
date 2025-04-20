import pandas as pd
import numpy as np
from tqdm import tqdm
import os

def load_excel_file(file_path):
    """加载Excel文件并进行数据验证和调试"""
    try:
        # ✅ 读取 Excel 文件
        df = pd.read_excel(file_path)

        # ✅ 调试技巧 3：强制转换金额字段，防止格式错误
        df['销售额'] = pd.to_numeric(df['销售额'], errors='coerce')

        # ✅ 打印格式错误警告（可选）
        if df['销售额'].isna().any():
            print(f"⚠️ {file_path} 中有格式错误的销售额数据，已转换为 NaN")

        # ✅ 过滤掉负值和 NaN 销售额
        invalid_rows = df[df['销售额'].isna() | (df['销售额'] < 0)]
        if not invalid_rows.empty:
            print(f"⚠️ {os.path.basename(file_path)} 中有 {len(invalid_rows)} 行无效销售额（负数或NaN），已跳过")
            df = df[df['销售额'].notna() & (df['销售额'] >= 0)]

        # ✅ 调试技巧 2：添加来源标记
        city_name = os.path.basename(file_path).split('_')[1].split('.')[0]
        df['城市'] = city_name
        df['来源文件'] = os.path.basename(file_path)

        # ✅ 调试技巧 1：在此设置断点调试并右键 → View as DataFrame
        return df
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return None

def process_sales_data():
    """处理销售数据并生成汇总结果"""
    beijing_file = 'sales_北京.xlsx'
    shanghai_file = 'sales_上海.xlsx'

    if not os.path.exists(beijing_file) or not os.path.exists(shanghai_file):
        print("❌ 找不到Excel文件，请确认 sales_北京.xlsx 和 sales_上海.xlsx 是否存在")
        return

    print("🔄 正在加载销售数据...")

    # 加载北京数据
    beijing_data = load_excel_file(beijing_file)
    if beijing_data is None:
        return

    # 加载上海数据
    shanghai_data = load_excel_file(shanghai_file)
    if shanghai_data is None:
        return

    # 合并数据
    combined_data = pd.concat([beijing_data, shanghai_data], ignore_index=True)

    # 按产品类别和城市汇总销售额
    summary_data = combined_data.groupby(['产品类别', '城市'])['销售额'].sum().reset_index()

    # 创建数据透视表
    pivot_data = summary_data.pivot(index='产品类别', columns='城市', values='销售额').reset_index()

    # 添加总计列
    pivot_data['总计'] = pivot_data[['北京', '上海']].sum(axis=1)

    # 保留两位小数
    for col in ['北京', '上海', '总计']:
        pivot_data[col] = pivot_data[col].round(2)

    # 保存结果
    with pd.ExcelWriter('sales_汇总.xlsx', engine='openpyxl') as writer:
        pivot_data.to_excel(writer, sheet_name='分析结果', index=False)
        combined_data.to_excel(writer, sheet_name='原始数据', index=False)

    print("✅ 汇总完成！结果已保存为 sales_汇总.xlsx")
    print("\n📊 汇总结果预览：")
    print(pivot_data)

if __name__ == "__main__":
    process_sales_data()
