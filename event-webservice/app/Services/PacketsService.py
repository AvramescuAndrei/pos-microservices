from typing import Dict, Any, List, Tuple, Optional

from app.Models.models import EventPacket
from app.Repositories.PacketsRepository import PacketsRepository

class PacketsService:
    @staticmethod
    def _packet_to_dict(packet: EventPacket) -> Dict[str, Any]:
        return {
            "ID": packet.ID,
            "nume": packet.nume,
            "descriere": packet.descriere,
            "numarLocuri": packet.numarLocuri,
            "_links": {
                "self": {
                    "href": f"/api/event-manager/event-packets/{packet.ID}"
                },
                "events": {
                    "href": f"/api/event-manager/event-packets/{packet.ID}/events"
                },
            },
        }

    @staticmethod
    def list_packets(page: int, items_per_page: int) -> Tuple[List[Dict[str, Any]], int]:
        packets, total = PacketsRepository.list_packets(page, items_per_page)
        return [PacketsService._packet_to_dict(p) for p in packets], total

    @staticmethod
    def get_packet(packet_id: int) -> Optional[Dict[str, Any]]:
        packet = PacketsRepository.get_packet(packet_id)
        if packet is None:
            return None
        return PacketsService._packet_to_dict(packet)

    @staticmethod
    def create_packet(data: dict) -> Dict[str, Any]:
        packet = PacketsRepository.create_packet(data)
        return PacketsService._packet_to_dict(packet)

    @staticmethod
    def replace_packet(packet_id: int, data: dict) -> Optional[Dict[str, Any]]:
        packet = PacketsRepository.replace_packet(packet_id, data)
        if packet is None:
            return None
        return PacketsService._packet_to_dict(packet)

    @staticmethod
    def delete_packet(packet_id: int) -> bool:
        return PacketsRepository.delete_packet(packet_id)

    @staticmethod
    def events_in_packet(packet_id: int) -> List[Dict[str, Any]]:
        events = PacketsRepository.list_events_for_packet(packet_id)
        result: List[Dict[str, Any]] = []
        for e in events:
            result.append(
                {
                    "ID": e.ID,
                    "ID_OWNER": e.ID_OWNER,
                    "nume": e.nume,
                    "locatie": e.locatie,
                    "descriere": e.descriere,
                    "numarLocuri": e.numarLocuri,
                    "_links": {
                        "self": {
                            "href": f"/api/event-manager/events/{e.ID}"
                        }
                    },
                }
            )
        return result
