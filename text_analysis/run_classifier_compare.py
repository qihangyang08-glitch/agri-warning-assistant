from pathlib import Path
import csv
import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CURRENT_DIR = Path(__file__).resolve().parent
RESOURCE_FILE = CURRENT_DIR / "resources" / "labeled_news.csv"
OUTPUT_DIR = CURRENT_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "classifier_compare.csv"
sys.path.insert(0, str(CURRENT_DIR))

from classifier import classify_news  # noqa: E402
from ml_classifier import SklearnTextClassifier  # noqa: E402


def load_labeled_rows() -> list[dict]:
    with open(RESOURCE_FILE, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def save_rows(rows: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = ["title", "label", "rule_prediction", "ml_prediction"]
    with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = load_labeled_rows()
    ml_classifier = SklearnTextClassifier()
    ml_classifier.train_from_csv(RESOURCE_FILE)

    compared = []
    for row in rows:
        title = row["title"]
        content = row["content"]
        compared.append(
            {
                "title": title,
                "label": row["label"],
                "rule_prediction": classify_news(title, content),
                "ml_prediction": ml_classifier.predict(title, content),
            }
        )

    save_rows(compared)
    rule_correct = sum(1 for row in compared if row["label"] == row["rule_prediction"])
    ml_correct = sum(1 for row in compared if row["label"] == row["ml_prediction"])

    print("分类器对比")
    print(f"样本数量: {len(compared)}")
    print(f"规则分类准确数: {rule_correct}/{len(compared)}")
    print(f"机器学习分类准确数: {ml_correct}/{len(compared)}")
    print(f"输出文件: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
