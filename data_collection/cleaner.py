import html
import re


_TAG_RE = re.compile(r"<[^>]+>")
_SPACE_RE = re.compile(r"\s+")


def clean_text(value: object) -> str:
    """Normalize scraped or imported text while keeping Chinese punctuation."""
    if value is None:
        return ""
    text = html.unescape(str(value))
    text = _TAG_RE.sub(" ", text)
    text = text.replace("\u3000", " ")
    text = _SPACE_RE.sub(" ", text)
    return text.strip()


def clean_news_row(row: dict) -> dict:
    return {
        "title": clean_text(row.get("title") or row.get("标题")),
        "content": clean_text(row.get("content") or row.get("正文")),
        "source": clean_text(row.get("source") or row.get("来源")),
        "publish_time": clean_text(row.get("publish_time") or row.get("发布时间")),
        "url": clean_text(row.get("url") or row.get("链接")),
        "region": clean_text(row.get("region") or row.get("地区")),
        "category": clean_text(row.get("category") or row.get("分类")),
    }


def clean_price_row(row: dict) -> dict:
    raw_price = clean_text(row.get("price") or row.get("价格") or "0")
    try:
        price = float(raw_price)
    except ValueError:
        price = 0.0

    return {
        "product_name": clean_text(row.get("product_name") or row.get("农产品名称")),
        "price": price,
        "unit": clean_text(row.get("unit") or row.get("单位")),
        "region": clean_text(row.get("region") or row.get("地区")),
        "date": clean_text(row.get("date") or row.get("日期")),
        "source": clean_text(row.get("source") or row.get("来源")),
    }

