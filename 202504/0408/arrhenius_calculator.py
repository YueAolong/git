import numpy as np
from scipy import stats

def celsius_to_kelvin(celsius):
    """将摄氏度转换为开尔文"""
    return celsius + 273.15

def calculate_activation_energy(temperatures, k_values):
    """
    使用阿伦尼乌斯方程计算活化能
    ln(k) = ln(A) - Ea/(RT)
    """
    R = 8.314  # 气体常数 (J/(mol·K))
    
    # 将温度转换为开尔文
    T_kelvin = [celsius_to_kelvin(t) for t in temperatures]
    
    # 计算 1/T 和 ln(k)
    x = [1/t for t in T_kelvin]
    y = [np.log(k) for k in k_values]
    
    # 使用线性回归计算斜率
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    # 计算活化能 (Ea = -slope * R)
    activation_energy = -slope * R
    
    return activation_energy, r_value**2

def main():
    print("欢迎使用阿伦尼乌斯方程活化能计算器！")
    print("请输入至少两组温度和对应的反应速率常数k值")
    print("输入完成后，输入'q'结束输入\n")
    
    temperatures = []
    k_values = []
    
    while True:
        try:
            # 获取温度输入
            temp_input = input("请输入温度（摄氏度）或输入'q'结束：")
            if temp_input.lower() == 'q':
                break
                
            temperature = float(temp_input)
            
            # 获取k值输入
            k_input = input("请输入对应的反应速率常数k值：")
            if k_input.lower() == 'q':
                break
                
            k_value = float(k_input)
            
            # 验证输入
            if k_value <= 0:
                print("错误：k值必须大于0！")
                continue
                
            temperatures.append(temperature)
            k_values.append(k_value)
            
        except ValueError:
            print("错误：请输入有效的数字！")
            continue
    
    # 检查是否有足够的数据
    if len(temperatures) < 2:
        print("错误：需要至少两组数据才能计算活化能！")
        return
    
    # 计算活化能
    activation_energy, r_squared = calculate_activation_energy(temperatures, k_values)
    
    # 输出结果
    print("\n计算结果：")
    print(f"活化能 (Ea) = {activation_energy:.2f} J/mol")
    print(f"活化能 (Ea) = {activation_energy/1000:.2f} kJ/mol")
    print(f"R² = {r_squared:.4f}")
    
    # 输出数据表
    print("\n输入数据：")
    print("温度(°C)\t温度(K)\t\tk值")
    print("-" * 40)
    for t, k in zip(temperatures, k_values):
        print(f"{t:.2f}\t\t{celsius_to_kelvin(t):.2f}\t\t{k:.6f}")

if __name__ == "__main__":
    main() 