from pathlib import Path
import csv
import sys

from dedup import deduplicate_news
from news_crawler import NewsCrawler
from sources import NEWS_SOURCES


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "crawler_news.csv"


def save_news(items: list[dict], path: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = ["title", "content", "source", "publish_time", "url", "region", "category"]
    with open(path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)


def main() -> None:
    crawler = NewsCrawler(timeout=12)
    result = crawler.crawl_sources(NEWS_SOURCES, limit_per_source=5)
    news = deduplicate_news(result.items)
    save_news(news, OUTPUT_FILE)

    print("联网爬虫验证")
    print(f"配置数据源数量: {len(NEWS_SOURCES)}")
    print(f"抓取新闻数量: {len(news)}")
    print(f"输出文件: {OUTPUT_FILE}")

    if result.errors:
        print("\n异常数据源:")
        for error in result.errors:
            print(f"- {error}")

    if news:
        print("\n新闻样例:")
        for item in news[:3]:
            print(f"- {item['title']} | {item['source']} | {item['url']}")
    else:
        print("\n没有抓取到新闻，请检查网络、网站结构或数据源配置。")


if __name__ == "__main__":
    main()
