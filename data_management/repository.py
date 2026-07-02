from typing import Any

from db import ensure_warning_score_columns, ensure_warning_unique_key, get_connection


def _execute_many(sql: str, rows: list[dict]) -> int:
    if not rows:
        return 0
    with get_connection() as connection:
        with connection.cursor() as cursor:
            return cursor.executemany(sql, rows)


def clear_demo_data() -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM warnings")
            cursor.execute("DELETE FROM product_prices")
            cursor.execute("DELETE FROM news")


def insert_news(rows: list[dict]) -> int:
    sql = """
    INSERT INTO news
      (title, content, source, publish_time, url, region, category, summary, keywords)
    VALUES
      (%(title)s, %(content)s, %(source)s, %(publish_time)s, %(url)s, %(region)s,
       %(category)s, %(summary)s, %(keywords)s)
    ON DUPLICATE KEY UPDATE
      content = VALUES(content),
      source = VALUES(source),
      publish_time = VALUES(publish_time),
      region = VALUES(region),
      category = VALUES(category),
      summary = VALUES(summary),
      keywords = VALUES(keywords)
    """
    return _execute_many(sql, rows)


def insert_prices(rows: list[dict]) -> int:
    sql = """
    INSERT INTO product_prices
      (product_name, price, unit, region, date, source)
    VALUES
      (%(product_name)s, %(price)s, %(unit)s, %(region)s, %(date)s, %(source)s)
    ON DUPLICATE KEY UPDATE
      price = VALUES(price),
      unit = VALUES(unit)
    """
    return _execute_many(sql, rows)


def insert_warnings(rows: list[dict]) -> int:
    ensure_warning_score_columns()
    ensure_warning_unique_key()
    sql = """
    INSERT INTO warnings
      (title, region, product, risk_type, risk_score, risk_level, keyword_score,
       price_score, heat_score, region_score, positive_adjustment, trigger_words,
       reason, suggestion, source, category, url)
    VALUES
      (%(title)s, %(region)s, %(product)s, %(risk_type)s, %(risk_score)s,
       %(risk_level)s, %(keyword_score)s, %(price_score)s, %(heat_score)s,
       %(region_score)s, %(positive_adjustment)s, %(trigger_words)s, %(reason)s,
       %(suggestion)s, %(source)s, %(category)s, %(url)s)
    ON DUPLICATE KEY UPDATE
      title = VALUES(title),
      region = VALUES(region),
      product = VALUES(product),
      risk_score = VALUES(risk_score),
      risk_level = VALUES(risk_level),
      keyword_score = VALUES(keyword_score),
      price_score = VALUES(price_score),
      heat_score = VALUES(heat_score),
      region_score = VALUES(region_score),
      positive_adjustment = VALUES(positive_adjustment),
      trigger_words = VALUES(trigger_words),
      reason = VALUES(reason),
      suggestion = VALUES(suggestion),
      source = VALUES(source),
      category = VALUES(category)
    """
    return _execute_many(sql, rows)


def update_warning_score_parts(rows: list[dict]) -> int:
    ensure_warning_score_columns()
    sql = """
    UPDATE warnings
    SET risk_score = %(risk_score)s,
        risk_level = %(risk_level)s,
        keyword_score = %(keyword_score)s,
        price_score = %(price_score)s,
        heat_score = %(heat_score)s,
        region_score = %(region_score)s,
        positive_adjustment = %(positive_adjustment)s,
        trigger_words = %(trigger_words)s
    WHERE id = %(id)s
    """
    return _execute_many(sql, rows)


def fetch_all(sql: str, params: tuple[Any, ...] = ()) -> list[dict]:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return list(cursor.fetchall())


def fetch_one(sql: str, params: tuple[Any, ...] = ()) -> dict | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
