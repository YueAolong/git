import os
import requests
from bs4 import BeautifulSoup


def login_and_download(login_url, download_url, login_data, download_path):
    session = requests.Session()

    # 登录
    try:
        print("正在登录...")
        response = session.post(login_url, data=login_data)
        response.raise_for_status()

        # 检查是否登录成功
        if "登录" not in response.text:
            print("登录成功")
        else:
            print("登录失败")
            return

    except Exception as e:
        print(f"登录失败：{e}")
        return

    # 下载文件
    os.makedirs(download_path, exist_ok=True)
    file_name = os.path.join(download_path, download_url.split("/")[-1])

    try:
        print(f"正在下载：{file_name}")
        response = session.get(download_url)
        response.raise_for_status()

        with open(file_name, "wb") as file:
            file.write(response.content)
        print(f"下载完成：{file_name}")

    except Exception as e:
        print(f"下载失败：{download_url} - {e}")


if __name__ == "__main__":
    # 登录页面URL
    login_url = "https://gms.bit.edu.cn/gmsstu/login"

    # 示例：文件下载路径（登录后访问的链接）
    download_url = "https://gms.bit.edu.cn/gmsstu/index/file.pdf"

    # 模拟登录数据
    login_data = {
        "username": "3220222256",
        "password": "Lilingxuan!1",
        # 如果有验证码，可以通过分析页面获取验证码字段
    }

    # 下载文件路径
    download_path = "downloads"

    login_and_download(login_url, download_url, login_data, download_path)
