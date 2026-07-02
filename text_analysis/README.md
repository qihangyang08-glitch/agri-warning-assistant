# 文本分析模块

本模块负责农业新闻的分词、停用词过滤、关键词提取、摘要生成和新闻分类。

## 目录结构

```text
text_analysis/
├─ __init__.py
├─ analyzer.py
├─ classifier.py
├─ keywords.py
├─ ml_classifier.py
├─ run_analysis.py
├─ summarizer.py
├─ tokenizer.py
├─ resources/
│  ├─ agriculture_keywords.txt
│  ├─ labeled_news.csv
│  └─ stopwords.txt
└─ output/
   └─ analyzed_news.csv
```

## 运行方式

在项目根目录执行：

```bash
D:\Develop\Tools\agri-warning-venv\Scripts\python.exe project\text_analysis\run_analysis.py
```

运行后会读取第一模块中的演示新闻：

```text
project/data_collection/sample_data/sample_news.csv
```

并输出分析结果到：

```text
project/text_analysis/output/analyzed_news.csv
```

## 输出字段

| 字段 | 说明 |
| --- | --- |
| title | 新闻标题 |
| source | 新闻来源 |
| publish_time | 发布时间 |
| url | 新闻链接 |
| region | 地区 |
| category | 自动分类 |
| summary | 自动摘要 |
| keywords | 关键词 |

## 说明

当前版本以稳定可运行为主：

- 分词优先使用 `jieba`
- 关键词提取使用 TF-IDF 思路
- 摘要使用句子打分的抽取式摘要
- 分类使用农业领域关键词规则
- `ml_classifier.py` 提供机器学习分类样例接口

## 分类器对比

如需对比规则分类和机器学习分类，可执行：

```bash
D:\Develop\Tools\agri-warning-venv\Scripts\python.exe project\text_analysis\run_classifier_compare.py
```

结果会保存到：

```text
project/text_analysis/output/classifier_compare.csv
```
