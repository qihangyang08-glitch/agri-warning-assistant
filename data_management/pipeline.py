from pathlib import Path
import csv
import sys


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CURRENT_DIR.parent
DATA_COLLECTION_DIR = PROJECT_DIR / "data_collection"
TEXT_ANALYSIS_DIR = PROJECT_DIR / "text_analysis"
RISK_WARNING_DIR = PROJECT_DIR / "risk_warning"

sys.path.insert(0, str(DATA_COLLECTION_DIR))
sys.path.insert(0, str(TEXT_ANALYSIS_DIR))
sys.path.insert(0, str(RISK_WARNING_DIR))

from dedup import deduplicate_news, deduplicate_prices  # noqa: E402
from importers import import_news, import_prices  # noqa: E402
from analyzer import analyze_news_batch  # noqa: E402
from price_monitor import build_price_change_map  # noqa: E402
from warning_generator import generate_warnings  # noqa: E402
from repository import clear_demo_data, insert_news, insert_prices, insert_warnings  # noqa: E402


NEWS_INPUT = DATA_COLLECTION_DIR / "sample_data" / "sample_news.csv"
PRICE_INPUT = DATA_COLLECTION_DIR / "sample_data" / "sample_prices.csv"


def rebuild_from_demo_data(clear_first: bool = True) -> dict:
    raw_news = deduplicate_news(import_news(NEWS_INPUT))
    analyzed_news = analyze_news_batch(raw_news)

    raw_prices = deduplicate_prices(import_prices(PRICE_INPUT))
    price_changes = build_price_change_map(raw_prices)
    warnings = generate_warnings(analyzed_news, price_changes)

    news_for_db = []
    raw_by_url = {item.get("url", ""): item for item in raw_news}
    for item in analyzed_news:
        raw = raw_by_url.get(item.get("url", ""), {})
        news_for_db.append(
            {
                "title": item.get("title", ""),
                "content": raw.get("content", ""),
                "source": item.get("source", ""),
                "publish_time": item.get("publish_time", ""),
                "url": item.get("url", ""),
                "region": item.get("region", ""),
                "category": item.get("category", ""),
                "summary": item.get("summary", ""),
                "keywords": item.get("keywords", ""),
            }
        )

    if clear_first:
        clear_demo_data()

    return {
        "news": insert_news(news_for_db),
        "prices": insert_prices(raw_prices),
        "warnings": insert_warnings(warnings),
    }


def read_csv_rows(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))

