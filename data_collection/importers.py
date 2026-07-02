import csv
from pathlib import Path

from cleaner import clean_news_row, clean_price_row


def _read_csv(path: str | Path) -> list[dict]:
    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _read_excel(path: str | Path) -> list[dict]:
    try:
        import pandas as pd
    except ImportError as exc:
        raise RuntimeError("导入 Excel 需要安装 pandas 和 openpyxl。") from exc

    frame = pd.read_excel(path)
    frame = frame.fillna("")
    return frame.to_dict(orient="records")


def read_table(path: str | Path) -> list[dict]:
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        return _read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return _read_excel(path)
    raise ValueError(f"暂不支持的文件类型: {suffix}")


def import_news(path: str | Path) -> list[dict]:
    rows = read_table(path)
    return [row for row in (clean_news_row(row) for row in rows) if row["title"]]


def import_prices(path: str | Path) -> list[dict]:
    rows = read_table(path)
    return [
        row
        for row in (clean_price_row(row) for row in rows)
        if row["product_name"] and row["price"] > 0
    ]

