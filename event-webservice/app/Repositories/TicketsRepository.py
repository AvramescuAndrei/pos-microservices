from typing import List, Optional, Tuple

from app.DB.database import db
from app.Models.models import Ticket

class TicketsRepository:
    @staticmethod
    def list_tickets(page: int, items_per_page: int) -> Tuple[List[Ticket], int]:
        query = Ticket.select().order_by(Ticket.COD)
        total = query.count()

        if items_per_page > 0:
            tickets = list(query.paginate(page, items_per_page))
        else:
            tickets = list(query)

        return tickets, total

    @staticmethod
    def get_ticket(cod: str) -> Optional[Ticket]:
        return Ticket.get_or_none(Ticket.COD == cod)

    @staticmethod
    def create_ticket(data: dict) -> Ticket:
        mapped = {
            "COD": data.get("COD"),
            "event_id": data.get("EvenimentID"),
            "packet_id": data.get("PachetID"),
            "valid": data.get("valid", True),
        }
        with db.atomic():
            return Ticket.create(**mapped)

    @staticmethod
    def invalidate_ticket(cod: str) -> bool:
        with db.atomic():
            ticket = TicketsRepository.get_ticket(cod)
            if ticket is None:
                return False

            ticket.valid = False
            ticket.save()
            return True

    @staticmethod
    def create_ticket_with_code(code: str, event_id: Optional[int], packet_id: Optional[int], valid: bool = True) -> Ticket:
        with db.atomic():
            return Ticket.create(
                COD=code,
                event_id=event_id,
                packet_id=packet_id,
                valid=valid,
            )
