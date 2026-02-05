from __future__ import annotations
from typing import List, Tuple, Optional

from app.DB.database import db
from app.Models.models import Event, EventPacket


class PacketsRepository:
    @staticmethod
    def list_packets(page: int, items_per_page: int) -> Tuple[List[EventPacket], int]:
        query = EventPacket.select().order_by(EventPacket.ID)
        total = query.count()

        packets = (
            query.paginate(page, items_per_page)
            if items_per_page > 0
            else list(query)
        )

        return list(packets), total

    @staticmethod
    def get_packet(packet_id: int) -> Optional[EventPacket]:
        return EventPacket.get_or_none(EventPacket.ID == packet_id)

    @staticmethod
    def create_packet(data: dict) -> EventPacket:
        with db.atomic():
            return EventPacket.create(**data)

    @staticmethod
    def replace_packet(packet_id: int, data: dict) -> Optional[EventPacket]:
        with db.atomic():
            packet = PacketsRepository.get_packet(packet_id)
            if packet is None:
                return None

            for key, value in data.items():
                setattr(packet, key, value)
            packet.save()
            return packet

    @staticmethod
    def delete_packet(packet_id: int) -> bool:
        with db.atomic():
            deleted = EventPacket.delete().where(EventPacket.ID == packet_id).execute()
            return deleted > 0

    @staticmethod
    def list_events_for_packet(packet_id: int) -> List[Event]:
        query = (
            Event
            .select()
            .where(Event.PachetID == packet_id)
            .order_by(Event.ID)
        )
        return list(query)
