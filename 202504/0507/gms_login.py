from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

def setup_driver(download_path):
    chrome_options = Options()
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_to_gms(driver, username, password):
    try:
        driver.get('https://gms.bit.edu.cn/gmsstu/index')
        wait = WebDriverWait(driver, 10)

        # 切换到 iframe（如果存在）
        try:
            iframe = wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
            print("Switched to iframe.")
        except Exception:
            print("No iframe found, proceeding...")

        # 输入用户名
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        username_field.send_keys(username)

        # 输入密码
        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys(password)

        # 点击登录按钮
        try:
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '登录')]")))
            login_button.click()
        except Exception as e:
            print(f"Login button not clickable: {str(e)}")

        time.sleep(2)
        print("Login successful.")
        return True

    except Exception as e:
        print(f"Error during login: {str(e)}")
        return False

def download_files(driver):
    try:
        # 示例：假设下载链接文字是“下载”
        file_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '下载')]"))
        )
        file_link.click()
        print("File download initiated.")
    except Exception as e:
        print(f"File download failed: {str(e)}")

if __name__ == "__main__":
    username = os.getenv('GMS_USERNAME') or input("Enter your GMS username: ")
    password = os.getenv('GMS_PASSWORD') or input("Enter your GMS password: ")

    # 设置下载路径
    download_path = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_path, exist_ok=True)

    driver = setup_driver(download_path)

    if login_to_gms(driver, username, password):
        download_files(driver)

    input("Press Enter to close the browser...")
    driver.quit()
