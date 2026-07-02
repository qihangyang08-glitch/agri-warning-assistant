# 风险预警模块

本模块负责根据新闻分析结果、关键词、地区、农产品和价格变化生成农业风险预警。

## 运行方式

在项目根目录执行：

```bash
D:\Develop\Tools\agri-warning-venv\Scripts\python.exe project\risk_warning\run_warning.py
```

脚本会读取：

```text
project/text_analysis/output/analyzed_news.csv
project/data_collection/sample_data/sample_prices.csv
```

并输出：

```text
project/risk_warning/output/warnings.csv
```

## 风险评分规则

当前基础版风险分由以下部分构成：

```text
总风险分 = 风险关键词分 + 价格波动分 + 新闻热度分 + 地区集中度分
```

风险等级：

| 分数 | 等级 |
| --- | --- |
| 0-30 | 低风险 |
| 31-60 | 中风险 |
| 61-80 | 较高风险 |
| 81-100 | 高风险 |

## 输出字段

| 字段 | 说明 |
| --- | --- |
| title | 新闻标题 |
| region | 涉及地区 |
| product | 涉及农产品 |
| risk_type | 风险类型 |
| risk_score | 风险分数 |
| risk_level | 风险等级 |
| trigger_words | 触发关键词 |
| reason | 预警原因 |
| suggestion | 建议措施 |
| url | 新闻链接 |

