from hashlib import sha1


def news_key(item: dict) -> str:
    url = (item.get("url") or "").strip()
    if url:
        return f"url:{url}"

    title = (item.get("title") or "").strip()
    source = (item.get("source") or "").strip()
    publish_time = (item.get("publish_time") or "").strip()
    raw = "|".join([title, source, publish_time])
    return "title:" + sha1(raw.encode("utf-8")).hexdigest()


def deduplicate_news(items: list[dict]) -> list[dict]:
    seen = set()
    result = []
    for item in items:
        key = news_key(item)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def deduplicate_prices(items: list[dict]) -> list[dict]:
    seen = set()
    result = []
    for item in items:
        key = (
            item.get("product_name"),
            item.get("region"),
            item.get("date"),
            item.get("source"),
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result

