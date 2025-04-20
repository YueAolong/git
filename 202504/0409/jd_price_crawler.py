import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import random
import logging
from fake_useragent import UserAgent
from datetime import datetime
import os
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("jd_crawler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class JDPriceCrawler:
    def __init__(self, max_retries=3, timeout=10, delay_range=(1, 3)):
        self.max_retries = max_retries
        self.timeout = timeout
        self.delay_range = delay_range
        self.ua = UserAgent()
        self.session = requests.Session()

    def get_random_headers(self):
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }

    def random_delay(self, base_delay=0):
        delay = base_delay + random.uniform(self.delay_range[0], self.delay_range[1])
        logger.debug(f"等待 {delay:.2f} 秒...")
        time.sleep(delay)

    def get_product_price(self, product_id):
        url = f"https://item.jd.com/{product_id}.html"

        for attempt in range(self.max_retries):
            try:
                logger.info(f"获取商品 {product_id} 的价格 (第 {attempt+1} 次尝试)")

                # 指数退避 + 随机延时
                self.random_delay(base_delay=2 ** attempt)

                response = self.session.get(
                    url,
                    headers=self.get_random_headers(),
                    timeout=self.timeout
                )

                if response.status_code != 200:
                    logger.warning(f"请求失败，状态码: {response.status_code}")
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')

                # 标题容错处理
                title_tag = soup.select_one('.sku-name') or soup.select_one('.itemInfo-wrap .sku-name')
                title = title_tag.text.strip() if title_tag else "未知商品"

                # 价格 API 请求
                price_api_url = f"https://p.3.cn/prices/mgets?skuIds=J_{product_id}"
                price_response = self.session.get(
                    price_api_url,
                    headers=self.get_random_headers(),
                    timeout=self.timeout
                )

                if price_response.status_code == 200:
                    try:
                        price_data = price_response.json()
                        if price_data and len(price_data) > 0:
                            price = price_data[0].get('p', '未知价格')
                            original_price = price_data[0].get('op', '未知原价')
                            discount = "是" if price < original_price else "否"
                        else:
                            price = original_price = discount = '获取失败'
                    except ValueError:
                        price = original_price = discount = '解析失败'
                else:
                    price = original_price = discount = '请求失败'

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                return {
                    'product_id': product_id,
                    'title': title,
                    'price': price,
                    'original_price': original_price,
                    'discount': discount,
                    'crawl_time': current_time
                }

            except requests.exceptions.Timeout:
                logger.warning(f"请求超时 (尝试 {attempt+1})")
            except requests.exceptions.RequestException as e:
                logger.error(f"请求异常: {e}")
            except Exception as e:
                logger.error(f"未知错误: {e}")

        logger.error(f"获取商品 {product_id} 价格失败")
        return None

    def crawl_products(self, product_ids, output_csv='jd_prices.csv', output_json='jd_prices.json'):
        file_exists = os.path.isfile(output_csv)
        results = []

        with open(output_csv, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'product_id', 'title', 'price', 'original_price', 'discount', 'crawl_time'
            ])
            if not file_exists:
                writer.writeheader()

            for product_id in product_ids:
                result = self.get_product_price(product_id)
                if result:
                    writer.writerow(result)
                    results.append(result)
                    logger.info(f"✅ 成功获取 {product_id}：¥{result['price']}")
                else:
                    logger.error(f"❌ 获取失败：{product_id}")

        # 输出为 JSON 文件
        with open(output_json, 'w', encoding='utf-8') as jf:
            json.dump(results, jf, ensure_ascii=False, indent=4)

        logger.info(f"爬取完成，CSV 保存至 {output_csv}，JSON 保存至 {output_json}")


def main():
    # 支持命令行传参
    if len(sys.argv) > 1:
        product_ids = sys.argv[1:]
    else:
        product_ids = ['100012043978']  # 默认商品ID

    crawler = JDPriceCrawler(max_retries=3, timeout=10, delay_range=(1, 3))
    crawler.crawl_products(product_ids)


if __name__ == "__main__":
    main()
