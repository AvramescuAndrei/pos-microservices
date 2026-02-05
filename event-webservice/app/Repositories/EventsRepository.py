from typing import List, Tuple, Optional

from app.DB.database import db
from app.Models.models import Event, EventPacket

class EventsRepository:
    @staticmethod
    def list_events(page: int, items_per_page: int) -> Tuple[List[Event], int]:
        query = Event.select().order_by(Event.ID)
        total = query.count()

        events = (
            query.paginate(page, items_per_page)
            if items_per_page > 0
            else list(query)
        )

        return list(events), total

    @staticmethod
    def get_event(event_id: int) -> Optional[Event]:
        return Event.get_or_none(Event.ID == event_id)

    @staticmethod
    def create_event(data: dict) -> Event:
        with db.atomic():
            return Event.create(**data)

    @staticmethod
    def replace_event(event_id: int, data: dict) -> Optional[Event]:
        with db.atomic():
            event = EventsRepository.get_event(event_id)
            if event is None:
                return None

            for key, value in data.items():
                setattr(event, key, value)
            event.save()
            return event

    @staticmethod
    def delete_event(event_id: int) -> bool:
        with db.atomic():
            deleted = Event.delete().where(Event.ID == event_id).execute()
            return deleted > 0

    @staticmethod
    def list_packets_for_event(event_id: int) -> List[EventPacket]:
        query = (
            EventPacket
            .select()
            .where(EventPacket.EvenimentID == event_id)
            .order_by(EventPacket.ID)
        )
        return list(query)
