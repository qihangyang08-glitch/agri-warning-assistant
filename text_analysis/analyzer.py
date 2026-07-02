from classifier import classify_news
from keywords import extract_keywords
from summarizer import summarize


def analyze_news_item(item: dict) -> dict:
    title = item.get("title", "")
    content = item.get("content", "")
    text = f"{title} {content}"
    keywords = extract_keywords(text)

    return {
        "title": title,
        "source": item.get("source", ""),
        "publish_time": item.get("publish_time", ""),
        "url": item.get("url", ""),
        "region": item.get("region", ""),
        "category": classify_news(title, content),
        "summary": summarize(title, content),
        "keywords": "、".join(keywords),
    }


def analyze_news_batch(items: list[dict]) -> list[dict]:
    return [analyze_news_item(item) for item in items]

