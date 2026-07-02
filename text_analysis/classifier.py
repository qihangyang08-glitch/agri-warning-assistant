CATEGORY_KEYWORDS = {
    "农业政策": ["政策", "补贴", "农业农村部", "通知", "部署", "扶持", "粮食安全"],
    "农产品价格": ["价格", "涨", "下跌", "上涨", "波动", "批发市场", "行情"],
    "病虫害": ["病虫害", "赤霉病", "虫害", "防治", "统防统治", "病害"],
    "气象灾害": ["降雨", "暴雨", "干旱", "洪涝", "排涝", "气象", "灾害"],
    "市场供需": ["供应", "销售", "订单", "电商", "渠道", "市场", "合作社"],
    "农业科技": ["技术", "专家", "管理", "监测", "机械", "智能", "科技"],
}


def classify_news(title: str, content: str) -> str:
    text = f"{title} {content}"
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(text.count(keyword) for keyword in keywords)

    category, score = max(scores.items(), key=lambda item: item[1])
    return category if score > 0 else "其他"

