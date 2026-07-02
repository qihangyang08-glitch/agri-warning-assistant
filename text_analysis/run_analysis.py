from pathlib import Path
import csv
import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CURRENT_DIR.parent
DATA_COLLECTION_DIR = PROJECT_DIR / "data_collection"
sys.path.insert(0, str(DATA_COLLECTION_DIR))

from importers import import_news  # noqa: E402
from dedup import deduplicate_news  # noqa: E402
from analyzer import analyze_news_batch  # noqa: E402


INPUT_FILE = DATA_COLLECTION_DIR / "sample_data" / "sample_news.csv"
OUTPUT_DIR = CURRENT_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "analyzed_news.csv"


def save_analysis(items: list[dict], path: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "title",
        "source",
        "publish_time",
        "url",
        "region",
        "category",
        "summary",
        "keywords",
    ]
    with open(path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)


def main() -> None:
    news = deduplicate_news(import_news(INPUT_FILE))
    analyzed = analyze_news_batch(news)
    save_analysis(analyzed, OUTPUT_FILE)

    print("文本分析模块演示")
    print(f"输入新闻数量: {len(news)}")
    print(f"输出分析数量: {len(analyzed)}")
    print(f"输出文件: {OUTPUT_FILE}")

    if analyzed:
        sample = analyzed[0]
        print("\n分析样例:")
        print(f"- 标题: {sample['title']}")
        print(f"- 分类: {sample['category']}")
        print(f"- 关键词: {sample['keywords']}")
        print(f"- 摘要: {sample['summary']}")


if __name__ == "__main__":
    main()
