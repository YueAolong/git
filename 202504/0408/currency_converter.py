import requests
from datetime import datetime

def get_exchange_rate():
    """从API获取实时汇率"""
    try:
        # 使用免费的汇率API
        url = "https://api.exchangerate-api.com/v4/latest/CNY"
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        return data['rates']['USD']
    except requests.RequestException as e:
        print(f"获取汇率时发生错误: {e}")
        return None

def convert_cny_to_usd(amount_cny):
    """将人民币转换为美元"""
    rate = get_exchange_rate()
    if rate is None:
        return None
    return amount_cny * rate

def main():
    print("欢迎使用人民币转美元计算器！")
    
    try:
        # 获取用户输入
        amount_cny = float(input("请输入人民币金额："))
        
        # 输入验证
        if amount_cny <= 0:
            print("错误：金额必须大于0！")
            return
            
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 转换并输出结果
        amount_usd = convert_cny_to_usd(amount_cny)
        if amount_usd is not None:
            print(f"\n转换时间：{current_time}")
            print(f"人民币：¥{amount_cny:,.2f}")
            print(f"美元：${amount_usd:,.2f}")
            
    except ValueError:
        print("错误：请输入有效的数字！")

if __name__ == "__main__":
    main() 