from typing import Dict


API_ROOT = "/api/event-manager"


def event_links(event_id: int) -> Dict[str, Dict[str, str]]:
    return {
        "self": {"href": f"{API_ROOT}/events/{event_id}"},
        "parent": {"href": f"{API_ROOT}/events"},
        "event-packets": {"href": f"{API_ROOT}/events/{event_id}/event-packets"},
        "tickets": {"href": f"{API_ROOT}/events/{event_id}/tickets"},
    }


def packet_links(packet_id: int) -> Dict[str, Dict[str, str]]:
    return {
        "self": {"href": f"{API_ROOT}/event-packets/{packet_id}"},
        "parent": {"href": f"{API_ROOT}/event-packets"},
        "events": {"href": f"{API_ROOT}/event-packets/{packet_id}/events"},
        "tickets": {"href": f"{API_ROOT}/event-packets/{packet_id}/tickets"},
    }


def ticket_links(cod: str) -> Dict[str, Dict[str, str]]:
    return {
        "self": {"href": f"{API_ROOT}/tickets/{cod}"},
        "parent": {"href": f"{API_ROOT}/tickets"},
    }


def list_links(resource: str, page: int, items_per_page: int, total_pages: int):
    base = f"{API_ROOT}/{resource}?page="
    links = {
        "self": {"href": f"{base}{page}&items_per_page={items_per_page}"},
    }
    if page > 1:
        links["prev"] = {
            "href": f"{base}{page-1}&items_per_page={items_per_page}"
        }
    if page < total_pages:
        links["next"] = {
            "href": f"{base}{page+1}&items_per_page={items_per_page}"
        }
    return links

def generate_client_links(email: str) -> Dict[str, Dict[str, str]]:
    base = "/clients"
    return {
        "self": {"href": f"{base}/{email}"},
        "update": {"href": f"{base}/{email}"},
        "delete": {"href": f"{base}/{email}"},
        "tickets": {"href": f"{base}/{email}/tickets"},
    }
