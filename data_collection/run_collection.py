from pathlib import Path
import sys

from dedup import deduplicate_news, deduplicate_prices
from importers import import_news, import_prices


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_DIR = BASE_DIR / "sample_data"


def load_demo_data() -> tuple[list[dict], list[dict]]:
    news = import_news(SAMPLE_DIR / "sample_news.csv")
    prices = import_prices(SAMPLE_DIR / "sample_prices.csv")
    return deduplicate_news(news), deduplicate_prices(prices)


def main() -> None:
    news, prices = load_demo_data()
    print("数据采集模块演示")
    print(f"新闻数量: {len(news)}")
    print(f"价格记录数量: {len(prices)}")

    if news:
        print("\n新闻样例:")
        sample = news[0]
        print(f"- 标题: {sample['title']}")
        print(f"- 来源: {sample['source']}")
        print(f"- 地区: {sample['region']}")

    if prices:
        print("\n价格样例:")
        sample = prices[0]
        print(f"- 农产品: {sample['product_name']}")
        print(f"- 价格: {sample['price']} {sample['unit']}")
        print(f"- 地区: {sample['region']}")


if __name__ == "__main__":
    main()
