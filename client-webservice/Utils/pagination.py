from math import ceil
from typing import Dict, Any, List, Tuple


def paginate_list(items: List[Any], page: int = 1, items_per_page: int = 10) -> Tuple[List[Any], int]:
    if page < 1:
        page = 1
    if items_per_page < 1:
        items_per_page = 10

    start = (page - 1) * items_per_page
    end = start + items_per_page
    return items[start:end], len(items)


def calc_pages(total_items: int, items_per_page: int) -> int:
    if items_per_page <= 0:
        return 1
    return max(1, ceil(total_items / items_per_page))


def list_links(resource: str, page: int, items_per_page: int, total_pages: int) -> Dict[str, Dict[str, str]]:
    base = f"/api/{resource}?page="
    links = {"self": {"href": f"{base}{page}&items_per_page={items_per_page}"}}
    if page > 1:
        links["prev"] = {"href": f"{base}{page-1}&items_per_page={items_per_page}"}
    if page < total_pages:
        links["next"] = {"href": f"{base}{page+1}&items_per_page={items_per_page}"}
    return links
