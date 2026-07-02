from collections import Counter
from math import log

from tokenizer import AGRICULTURE_WORDS, tokenize


def extract_keywords(text: str, top_k: int = 8) -> list[str]:
    tokens = tokenize(text)
    if not tokens:
        return []

    counts = Counter(tokens)
    total = sum(counts.values())
    scores = {}
    for token, count in counts.items():
        tf = count / total
        domain_boost = 1.8 if token in AGRICULTURE_WORDS else 1.0
        length_boost = 1.15 if len(token) >= 3 else 1.0
        scores[token] = tf * log(total + 1) * domain_boost * length_boost

    return [
        word
        for word, _ in sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_k]
    ]

