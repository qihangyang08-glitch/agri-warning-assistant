import re

from keywords import extract_keywords
from tokenizer import tokenize


SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？!?])")


def split_sentences(text: str) -> list[str]:
    sentences = [sentence.strip() for sentence in SENTENCE_SPLIT_RE.split(text or "")]
    return [sentence for sentence in sentences if len(sentence) >= 8]


def summarize(title: str, content: str, max_sentences: int = 2) -> str:
    sentences = split_sentences(content)
    if not sentences:
        return title.strip()

    keywords = set(extract_keywords(f"{title} {content}", top_k=10))
    scored = []
    for index, sentence in enumerate(sentences):
        tokens = tokenize(sentence)
        keyword_hits = sum(1 for token in tokens if token in keywords)
        position_score = 1.0 if index == 0 else 0.7
        length_score = min(len(sentence) / 80, 1.0)
        score = keyword_hits * 2 + position_score + length_score
        scored.append((score, index, sentence))

    selected = sorted(scored, key=lambda item: item[0], reverse=True)[:max_sentences]
    selected = sorted(selected, key=lambda item: item[1])
    return "".join(sentence for _, _, sentence in selected)

