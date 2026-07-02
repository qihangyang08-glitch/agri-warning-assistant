from dataclasses import asdict, dataclass


@dataclass
class NewsItem:
    title: str
    content: str = ""
    source: str = ""
    publish_time: str = ""
    url: str = ""
    region: str = ""
    category: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PriceItem:
    product_name: str
    price: float
    unit: str = ""
    region: str = ""
    date: str = ""
    source: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

