from collections import defaultdict


def build_price_change_map(price_items: list[dict]) -> dict[tuple[str, str], dict]:
    grouped = defaultdict(list)
    for item in price_items:
        product = item.get("product_name", "")
        region = item.get("region", "")
        if not product or not region:
            continue
        grouped[(product, region)].append(item)

    changes = {}
    for key, rows in grouped.items():
        rows = sorted(rows, key=lambda row: row.get("date", ""))
        if len(rows) < 2:
            continue
        first = float(rows[0].get("price", 0) or 0)
        last = float(rows[-1].get("price", 0) or 0)
        if first <= 0:
            continue
        change_rate = (last - first) / first
        changes[key] = {
            "first_price": first,
            "last_price": last,
            "change_rate": change_rate,
            "score": min(abs(change_rate) * 220, 25),
        }
    return changes


def find_price_signal(product: str, region: str, price_changes: dict[tuple[str, str], dict]) -> dict:
    if not product:
        return {}
    exact = price_changes.get((product, region))
    if exact:
        return exact
    for (price_product, price_region), signal in price_changes.items():
        if price_product == product and (not region or region in price_region or price_region in region):
            return signal
    return {}

