# 数据采集模块

本模块负责农业新闻、农业风险信息和农产品价格数据的获取、导入、清洗与去重。

## 已包含内容

- 新闻数据字段定义
- 农产品价格字段定义
- 新闻来源配置
- 新闻网页爬虫框架
- 新闻详情页解析
- CSV / Excel 导入工具
- 文本清洗工具
- 新闻去重工具
- 离线演示数据

## 目录结构

```text
data_collection/
├─ __init__.py
├─ cleaner.py
├─ dedup.py
├─ importers.py
├─ models.py
├─ news_crawler.py
├─ run_collection.py
├─ sources.py
└─ sample_data/
   ├─ sample_news.csv
   └─ sample_prices.csv
```

## 推荐使用方式

在项目根目录执行：

```bash
python project/data_collection/run_collection.py
```

该命令会读取 `sample_data` 中的演示数据，完成清洗和去重，并输出采集结果概览。

## 联网爬虫验证

如果已经安装 `requests` 和 `beautifulsoup4`，可以执行：

```bash
python project/data_collection/run_crawler_check.py
```

该命令会读取 `sources.py` 中配置的新闻源，尝试联网抓取新闻，并把结果保存到：

```text
project/data_collection/output/crawler_news.csv
```

如果输出的“抓取新闻数量”大于 0，并且 `crawler_news.csv` 中有标题和链接，说明真实联网爬取功能可用。

## 依赖说明

基础 CSV 导入只使用 Python 标准库。

如果要使用网页爬虫，需要安装：

```bash
pip install requests beautifulsoup4
```

如果要导入 Excel 文件，需要安装：

```bash
pip install pandas openpyxl
```

## 数据字段

### 新闻字段

| 字段 | 说明 |
| --- | --- |
| title | 新闻标题 |
| content | 新闻正文 |
| source | 新闻来源 |
| publish_time | 发布时间 |
| url | 新闻链接 |
| region | 地区 |
| category | 初始分类 |

### 价格字段

| 字段 | 说明 |
| --- | --- |
| product_name | 农产品名称 |
| price | 价格 |
| unit | 单位 |
| region | 地区 |
| date | 日期 |
| source | 数据来源 |
