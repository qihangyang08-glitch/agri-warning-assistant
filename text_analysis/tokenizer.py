from pathlib import Path
import re


RESOURCE_DIR = Path(__file__).resolve().parent / "resources"
STOPWORDS_FILE = RESOURCE_DIR / "stopwords.txt"
AGRI_WORDS_FILE = RESOURCE_DIR / "agriculture_keywords.txt"


def load_word_set(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }


STOPWORDS = load_word_set(STOPWORDS_FILE)
AGRICULTURE_WORDS = load_word_set(AGRI_WORDS_FILE)


def _load_jieba():
    try:
        import jieba
    except ImportError:
        return None
    for word in AGRICULTURE_WORDS:
        jieba.add_word(word)
    return jieba


JIEBA = _load_jieba()


def tokenize(text: str) -> list[str]:
    if not text:
        return []

    if JIEBA:
        raw_tokens = JIEBA.lcut(text)
    else:
        raw_tokens = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z0-9]+", text)

    tokens = []
    for token in raw_tokens:
        token = token.strip()
        if not token:
            continue
        if token in STOPWORDS:
            continue
        if len(token) < 2 and token not in AGRICULTURE_WORDS:
            continue
        if re.fullmatch(r"\W+", token):
            continue
        tokens.append(token)
    return tokens

