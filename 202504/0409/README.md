# 京东商品价格爬虫

这是一个用于爬取京东商品价格的Python爬虫程序。它可以根据商品ID获取当前价格，并将结果保存到CSV文件中。

## 功能特点

- 使用requests和BeautifulSoup爬取京东商品价格
- 支持根据商品ID获取当前价格
- 添加随机User-Agent和请求间隔，避免被反爬
- 结果保存到CSV文件
- 处理超时和重试机制
- 详细的日志记录

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 直接运行脚本，使用示例商品ID：

```bash
python jd_price_crawler.py
```

2. 修改代码中的商品ID列表，爬取多个商品：

```python
# 在main()函数中修改product_ids列表
product_ids = ['100012043978', '100012043979', '100012043980']
```

3. 自定义爬虫参数：

```python
# 创建爬虫实例时可以自定义参数
crawler = JDPriceCrawler(
    max_retries=5,  # 最大重试次数
    timeout=15,     # 请求超时时间(秒)
    delay_range=(2, 5)  # 请求间隔范围(秒)
)
```

## 输出结果

爬虫会将结果保存到`jd_prices.csv`文件中，包含以下字段：

- product_id: 商品ID
- title: 商品标题
- price: 商品价格
- crawl_time: 爬取时间

同时，程序运行日志会保存在`jd_crawler.log`文件中。

## 注意事项

1. 请合理设置请求间隔，避免对京东服务器造成过大压力
2. 京东可能会更新其网页结构，如果爬虫失效，请检查并更新相应的选择器
3. 本程序仅供学习和研究使用，请勿用于商业用途
4. 遵守京东的使用条款和robots.txt规则 