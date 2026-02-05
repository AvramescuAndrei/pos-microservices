from math import ceil
from typing import Tuple, List


def paginate(query, page: int = 1, items_per_page: int = 10) -> Tuple[List, int]:
    if page < 1:
        page = 1
    if items_per_page < 1:
        items_per_page = 10

    total_count = query.count()
    items = list(query.paginate(page, items_per_page))
    return items, total_count


def calc_pages(total_items: int, items_per_page: int) -> int:
    if items_per_page <= 0:
        return 1
    return max(1, ceil(total_items / items_per_page))
