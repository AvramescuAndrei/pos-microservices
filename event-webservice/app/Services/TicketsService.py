from typing import Dict, Any, List, Tuple, Optional

from app.Models.models import Ticket
from app.Repositories.TicketsRepository import TicketsRepository

class TicketsService:
    @staticmethod
    def _ticket_to_dict(ticket: Ticket) -> Dict[str, Any]:
        return {
            "COD": ticket.COD,
            "EvenimentID": ticket.event_id,
            "PachetID": ticket.packet_id,
            "valid": ticket.valid,
            "_links": {
                "self": {"href": f"/api/event-manager/tickets/{ticket.COD}"},
                "parent": {"href": "/api/event-manager/tickets"},
            },
        }

    @staticmethod
    def list_tickets(page: int, items_per_page: int) -> Tuple[List[Dict[str, Any]], int]:
        tickets, total = TicketsRepository.list_tickets(page, items_per_page)
        return [TicketsService._ticket_to_dict(t) for t in tickets], total

    @staticmethod
    def get_ticket(cod: str) -> Optional[Dict[str, Any]]:
        ticket = TicketsRepository.get_ticket(cod)
        if ticket is None:
            return None
        return TicketsService._ticket_to_dict(ticket)

    @staticmethod
    def create_ticket(data: dict) -> Dict[str, Any]:
        ticket = TicketsRepository.create_ticket(data)
        return TicketsService._ticket_to_dict(ticket)

    @staticmethod
    def invalidate_ticket(cod: str) -> bool:
        return TicketsRepository.invalidate_ticket(cod)
