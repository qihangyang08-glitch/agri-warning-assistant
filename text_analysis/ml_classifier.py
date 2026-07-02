from pathlib import Path


RESOURCE_DIR = Path(__file__).resolve().parent / "resources"
LABELED_FILE = RESOURCE_DIR / "labeled_news.csv"


class SklearnTextClassifier:
    """Small optional ML classifier for later comparison with rule results."""

    def __init__(self):
        self.pipeline = None

    def train_from_csv(self, path: Path = LABELED_FILE) -> None:
        try:
            import pandas as pd
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.linear_model import LogisticRegression
            from sklearn.pipeline import Pipeline
        except ImportError as exc:
            raise RuntimeError("机器学习分类需要安装 pandas 和 scikit-learn。") from exc

        frame = pd.read_csv(path)
        texts = (frame["title"].fillna("") + " " + frame["content"].fillna("")).tolist()
        labels = frame["label"].tolist()
        self.pipeline = Pipeline(
            [
                ("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(2, 4))),
                ("model", LogisticRegression(max_iter=500)),
            ]
        )
        self.pipeline.fit(texts, labels)

    def predict(self, title: str, content: str) -> str:
        if self.pipeline is None:
            self.train_from_csv()
        return self.pipeline.predict([f"{title} {content}"])[0]

