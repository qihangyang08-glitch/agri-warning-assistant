# 数据管理模块

本模块使用 MySQL 负责系统数据存储、查询接口和基础业务逻辑。

## 一、环境变量配置

请在 PowerShell 中按你的 MySQL 实际信息设置：

```powershell
$env:AGRI_DB_HOST="127.0.0.1"
$env:AGRI_DB_PORT="3306"
$env:AGRI_DB_USER="root"
$env:AGRI_DB_PASSWORD="你的MySQL密码"
$env:AGRI_DB_NAME="agri_warning"
```

如果不设置，程序默认使用：

```text
host=127.0.0.1
port=3306
user=root
password=
database=agri_warning
```

## 二、初始化数据库

先确保 MySQL 服务已启动，然后执行：

```bash
D:\Develop\Tools\agri-warning-venv\Scripts\python.exe project\data_management\run_init_mysql.py
```

该脚本会：

1. 创建数据库 `agri_warning`
2. 创建新闻表 `news`
3. 创建农产品价格表 `product_prices`
4. 创建风险预警表 `warnings`
5. 读取前三个模块的 CSV 结果并写入 MySQL

## 三、启动接口服务

```bash
D:\Develop\Tools\agri-warning-venv\Scripts\python.exe -m uvicorn project.data_management.app:app --reload --port 8000
```

启动后访问：

```text
http://127.0.0.1:8000/docs
```

即可查看 FastAPI 自动生成的接口文档。

## 四、主要接口

| 接口 | 说明 |
| --- | --- |
| `GET /api/health` | 健康检查 |
| `GET /api/news` | 新闻列表 |
| `GET /api/news/{id}` | 新闻详情 |
| `GET /api/warnings` | 风险预警列表 |
| `GET /api/prices` | 农产品价格列表 |
| `GET /api/stats/overview` | 首页统计 |
| `GET /api/charts/category` | 新闻分类统计 |
| `GET /api/charts/price-trend` | 价格趋势 |
| `GET /api/charts/hotwords` | 热点关键词 |
| `POST /api/pipeline/rebuild` | 重新从 CSV 导入数据 |

