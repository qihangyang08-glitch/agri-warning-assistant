from datetime import date

from repository import fetch_all, fetch_one


def list_news(keyword: str = "", category: str = "", region: str = "", limit: int = 20, offset: int = 0):
    sql = "SELECT * FROM news WHERE 1=1"
    params = []
    if keyword:
        sql += " AND (title LIKE %s OR content LIKE %s OR keywords LIKE %s)"
        like = f"%{keyword}%"
        params.extend([like, like, like])
    if category:
        sql += " AND category = %s"
        params.append(category)
    if region:
        sql += " AND region LIKE %s"
        params.append(f"%{region}%")
    sql += " ORDER BY id DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    return fetch_all(sql, tuple(params))


def get_news(news_id: int):
    return fetch_one("SELECT * FROM news WHERE id = %s", (news_id,))


def list_warnings(risk_level: str = "", region: str = "", product: str = "", limit: int = 20):
    sql = "SELECT * FROM warnings WHERE 1=1"
    params = []
    if risk_level:
        sql += " AND risk_level = %s"
        params.append(risk_level)
    if region:
        sql += " AND region LIKE %s"
        params.append(f"%{region}%")
    if product:
        sql += " AND product LIKE %s"
        params.append(f"%{product}%")
    sql += " ORDER BY risk_score DESC, id DESC LIMIT %s"
    params.append(limit)
    return fetch_all(sql, tuple(params))


def list_prices(product_name: str = "", region: str = ""):
    sql = "SELECT * FROM product_prices WHERE 1=1"
    params = []
    if product_name:
        sql += " AND product_name = %s"
        params.append(product_name)
    if region:
        sql += " AND region LIKE %s"
        params.append(f"%{region}%")
    sql += " ORDER BY product_name, region, date"
    return fetch_all(sql, tuple(params))


def overview_stats():
    today = date.today().isoformat()
    return {
        "news_count": fetch_one("SELECT COUNT(*) AS count FROM news")["count"],
        "today_news_count": fetch_one(
            "SELECT COUNT(*) AS count FROM news WHERE publish_time = %s",
            (today,),
        )["count"],
        "warning_count": fetch_one("SELECT COUNT(*) AS count FROM warnings")["count"],
        "high_warning_count": fetch_one(
            "SELECT COUNT(*) AS count FROM warnings WHERE risk_level IN ('较高风险', '高风险')"
        )["count"],
        "price_count": fetch_one("SELECT COUNT(*) AS count FROM product_prices")["count"],
    }


def category_chart():
    return fetch_all(
        "SELECT category AS name, COUNT(*) AS value FROM news GROUP BY category ORDER BY value DESC"
    )


def price_trend(product_name: str = ""):
    sql = """
    SELECT product_name, region, date, price, unit
    FROM product_prices
    WHERE 1=1
    """
    params = []
    if product_name:
        sql += " AND product_name = %s"
        params.append(product_name)
    sql += " ORDER BY product_name, region, date"
    return fetch_all(sql, tuple(params))


def hotwords_chart(limit: int = 20):
    rows = fetch_all("SELECT keywords FROM news WHERE keywords IS NOT NULL AND keywords <> ''")
    counts = {}
    for row in rows:
        for word in row["keywords"].split("、"):
            word = word.strip()
            if not word:
                continue
            counts[word] = counts.get(word, 0) + 1
    return [
        {"name": word, "value": count}
        for word, count in sorted(counts.items(), key=lambda item: item[1], reverse=True)[:limit]
    ]
