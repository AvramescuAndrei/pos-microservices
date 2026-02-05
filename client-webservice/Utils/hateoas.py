from typing import Dict

API_ROOT = "/api"


def generate_client_links(email: str) -> Dict[str, Dict[str, str]]:
    base = f"{API_ROOT}/clients"
    return {
        "self": {"href": f"{base}/{email}"},
        "update": {"href": f"{base}/{email}"},
        "delete": {"href": f"{base}/{email}"},
        "tickets": {"href": f"{base}/{email}/tickets"},
        "list": {"href": f"{base}"},
    }
