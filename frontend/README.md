# 前端展示模块

本模块是一个轻量级前端页面，使用 Vue 3 CDN 和 ECharts CDN 构建，不需要 `npm install`。

## 启动后端

先确保 MySQL 服务运行，然后在项目根目录执行：

```bash
D:\Develop\Tools\agri-warning-venv\Scripts\python.exe -m uvicorn project.data_management.app:app --reload --port 8000
```

## 启动前端

在项目根目录执行：

```bash
D:\Develop\Tools\agri-warning-venv\Scripts\python.exe -m http.server 5173 -d project/frontend
```

浏览器访问：

```text
http://127.0.0.1:5173
```

## 页面功能

- 首页统计
- 新闻分类图
- 农产品价格趋势图
- 热点关键词图
- 新闻列表与详情
- 风险预警列表
- 价格趋势表格
- 数据导入
- 立即更新新闻

