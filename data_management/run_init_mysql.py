import sys

from db import initialize_schema
from pipeline import rebuild_from_demo_data


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    initialize_schema()
    result = rebuild_from_demo_data(clear_first=True)
    print("MySQL 数据管理模块初始化完成")
    print(f"新闻入库: {result['news']}")
    print(f"价格入库: {result['prices']}")
    print(f"预警入库: {result['warnings']}")


if __name__ == "__main__":
    main()

