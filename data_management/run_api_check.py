import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from queries import category_chart, hotwords_chart, list_news, list_warnings, overview_stats, price_trend


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    print("数据管理模块查询验证")
    print(f"首页统计: {overview_stats()}")
    print(f"新闻数量样例: {len(list_news(limit=5))}")
    print(f"预警数量样例: {len(list_warnings(limit=5))}")
    print(f"分类图表: {category_chart()}")
    print(f"价格趋势样例数量: {len(price_trend())}")
    print(f"热点词样例: {hotwords_chart(limit=5)}")


if __name__ == "__main__":
    main()

