from typing import Dict, Any, List, Tuple, Optional

from app.Models.models import Event
from app.Repositories.EventsRepository import EventsRepository

class EventsService:
    @staticmethod
    def _event_to_dict(event: Event) -> Dict[str, Any]:
        return {
            "ID": event.ID,
            "ID_OWNER": event.ID_OWNER,
            "nume": event.nume,
            "locatie": event.locatie,
            "descriere": event.descriere,
            "numarLocuri": event.numarLocuri,
            "_links": {
                "self": {
                    "href": f"/api/event-manager/events/{event.ID}"
                },
                "event-packets": {
                    "href": f"/api/event-manager/events/{event.ID}/event-packets"
                },
                "tickets": {
                    "href": f"/api/event-manager/events/{event.ID}/tickets"
                },
            },
        }

    @staticmethod
    def list_events(page: int, items_per_page: int) -> Tuple[List[Dict[str, Any]], int]:
        events, total = EventsRepository.list_events(page, items_per_page)
        return [EventsService._event_to_dict(e) for e in events], total

    @staticmethod
    def get_event(event_id: int) -> Optional[Dict[str, Any]]:
        event = EventsRepository.get_event(event_id)
        if event is None:
            return None
        return EventsService._event_to_dict(event)

    @staticmethod
    def create_event(data: dict) -> Dict[str, Any]:
        event = EventsRepository.create_event(data)
        return EventsService._event_to_dict(event)

    @staticmethod
    def replace_event(event_id: int, data: dict) -> Optional[Dict[str, Any]]:
        event = EventsRepository.replace_event(event_id, data)
        if event is None:
            return None
        return EventsService._event_to_dict(event)

    @staticmethod
    def delete_event(event_id: int) -> bool:
        return EventsRepository.delete_event(event_id)

    @staticmethod
    def event_packets(event_id: int) -> List[Dict[str, Any]]:
        packets = EventsRepository.list_packets_for_event(event_id)
        result: List[Dict[str, Any]] = []
        for p in packets:
            result.append(
                {
                    "ID": p.ID,
                    "nume": p.nume,
                    "descriere": p.descriere,
                    "numarLocuri": p.numarLocuri,
                    "_links": {
                        "self": {
                            "href": f"/api/event-manager/event-packets/{p.ID}"
                        },
                        "events": {
                            "href": f"/api/event-manager/event-packets/{p.ID}/events"
                        },
                    },
                }
            )
        return result
