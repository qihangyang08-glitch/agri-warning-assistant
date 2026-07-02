from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urljoin

from cleaner import clean_text


BAD_TITLE_KEYWORDS = {
    "English",
    "邮箱",
    "举报中心",
    "中国农业农村信息网",
    "友情链接",
    "网站地图",
    "导报",
    "信用合作报",
}

BAD_URL_KEYWORDS = {
    "mail.",
    "english.",
    "12377.cn",
}


@dataclass
class CrawlResult:
    items: list[dict]
    errors: list[str]


class NewsCrawler:
    """A lightweight crawler for public agriculture news pages.

    The parser is intentionally conservative because government/news pages
    often have different structures. It extracts common article links from a
    list page, then tries several common selectors for article metadata.
    """

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def crawl_sources(self, sources: Iterable[dict], limit_per_source: int = 10) -> CrawlResult:
        items: list[dict] = []
        errors: list[str] = []
        for source in sources:
            try:
                items.extend(self.crawl_source(source, limit_per_source))
            except Exception as exc:  # Keep one source failure from stopping the batch.
                errors.append(f"{source.get('name', 'unknown')}: {exc}")
        return CrawlResult(items=items, errors=errors)

    def crawl_source(self, source: dict, limit: int = 10) -> list[dict]:
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError as exc:
            raise RuntimeError("网页爬虫需要安装 requests 和 beautifulsoup4。") from exc

        response = requests.get(source["list_url"], timeout=self.timeout)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")

        links = self._extract_links(soup, source, limit)
        items = []
        for url, title in links:
            try:
                item = self.fetch_detail(url, source)
                if not item["title"]:
                    item["title"] = title
                items.append(item)
            except Exception:
                continue
        return items

    def fetch_detail(self, url: str, source: dict) -> dict:
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")

        title = self._pick_text(soup, ["h1", ".title", "#title"])
        content = self._pick_article_text(soup)
        publish_time = self._pick_text(soup, [".time", ".date", ".source", ".info"])

        return {
            "title": clean_text(title),
            "content": clean_text(content),
            "source": source.get("name", ""),
            "publish_time": clean_text(publish_time),
            "url": url,
            "region": source.get("region", ""),
            "category": source.get("category", ""),
        }

    def _extract_links(self, soup, source: dict, limit: int) -> list[tuple[str, str]]:
        links = []
        for anchor in soup.find_all("a"):
            title = clean_text(anchor.get_text(" "))
            href = anchor.get("href")
            url = urljoin(source.get("base_url") or source["list_url"], href)
            if self._is_probable_news_link(title, url):
                links.append((url, title))
            if len(links) >= limit:
                break
        return links

    def _is_probable_news_link(self, title: str, url: str) -> bool:
        if not title or not url.startswith("http"):
            return False
        if len(title) < 8:
            return False
        if not re_search_chinese(title):
            return False
        if any(keyword in title for keyword in BAD_TITLE_KEYWORDS):
            return False
        if any(keyword in url for keyword in BAD_URL_KEYWORDS):
            return False
        return True

    def _pick_text(self, soup, selectors: list[str]) -> str:
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(" ")
        return ""

    def _pick_article_text(self, soup) -> str:
        selectors = ["article", ".article", ".content", "#content", ".TRS_Editor", ".main"]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(" ")
                if len(clean_text(text)) > 50:
                    return text
        paragraphs = [p.get_text(" ") for p in soup.find_all("p")]
        return " ".join(paragraphs)


def re_search_chinese(text: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in text)
