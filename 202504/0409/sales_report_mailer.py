import smtplib
import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import dotenv

def load_sales_data():
    """加载销售汇总数据"""
    try:
        # 读取汇总Excel文件
        df = pd.read_excel('sales_汇总.xlsx', sheet_name='分析结果')
        return df
    except Exception as e:
        print(f"读取销售数据时出错: {e}")
        return None

def create_html_table(df):
    """将DataFrame转换为HTML表格"""
    # 设置表格样式
    html_style = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: right;
        }
        th {
            background-color: #f2f2f2;
            text-align: center;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .total-row {
            font-weight: bold;
            background-color: #e6f2ff;
        }
    </style>
    """
    
    # 格式化数字列（添加千位分隔符和两位小数）
    for col in ['北京', '上海', '总计']:
        df[col] = df[col].apply(lambda x: f"{x:,.2f}")
    
    # 转换为HTML表格
    html_table = df.to_html(index=False, classes='sales-table')
    
    # 添加样式
    html_content = f"{html_style}\n{html_table}"
    
    return html_content

def send_email(recipient, subject, html_content, attachment_path=None):
    """发送HTML格式邮件"""
    # 加载环境变量
    dotenv.load_dotenv()
    
    # 获取邮箱配置
    sender = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASSWORD')
    
    if not sender or not password:
        print("错误：未设置邮箱环境变量，请设置EMAIL_USER和EMAIL_PASSWORD")
        return False
    
    try:
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # 添加HTML内容
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # 添加附件
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                attachment = MIMEApplication(f.read())
                attachment.add_header('Content-Disposition', 'attachment', 
                                    filename=os.path.basename(attachment_path))
                msg.attach(attachment)
        
        # 连接QQ邮箱SMTP服务器
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(sender, password)
        
        # 发送邮件
        server.send_message(msg)
        server.quit()
        
        print(f"邮件已成功发送至 {recipient}")
        return True
        
    except Exception as e:
        print(f"发送邮件时出错: {e}")
        return False

def main():
    # 加载销售数据
    sales_data = load_sales_data()
    if sales_data is None:
        return
    
    # 创建HTML内容
    today = datetime.now().strftime('%Y-%m-%d')
    html_content = f"""
    <html>
    <body>
        <h2>销售数据汇总报告 ({today})</h2>
        <p>尊敬的收件人：</p>
        <p>以下是今日销售数据汇总，详细数据请查看附件。</p>
        {create_html_table(sales_data)}
        <p>此致</p>
        <p>销售数据分析系统</p>
    </body>
    </html>
    """
    
    # 发送邮件
    recipient = input("请输入收件人邮箱: ")
    subject = f"销售数据汇总报告 ({today})"
    attachment_path = 'sales_汇总.xlsx'
    
    send_email(recipient, subject, html_content, attachment_path)

if __name__ == "__main__":
    main() 