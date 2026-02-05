import uuid
import httpx
import os
from fastapi import HTTPException

from DTO.schemas import ClientCreate, ClientUpdate, ClientOut, ClientTicket, TicketPurchase
from Repositories.ClientsRepository import ClientsRepository
from Utils.hateoas import generate_client_links

EVENT_WS_URL = os.getenv("EVENT_WS_URL", "http://127.0.0.1:8001/api/event-manager")


class ClientsService:
    def __init__(self):
        self.repo = ClientsRepository()

    def _to_out(self, data):
        return ClientOut(
            email=data["email"],
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            is_name_public=data.get("is_name_public", False),
            social_links=data.get("social_links"),
            is_social_public=data.get("is_social_public", False),
            tickets=data.get("tickets", []),
            _links=generate_client_links(data["email"]),
        )

    def create_client(self, payload: ClientCreate):
        if self.repo.get_client(payload.email):
            raise HTTPException(409, "Client already exists")
        return self._to_out(self.repo.create_client(payload))

    def get_clients(self):
        return [self._to_out(c) for c in self.repo.get_all_clients()]

    def get_client(self, email):
        c = self.repo.get_client(email)
        if not c:
            raise HTTPException(404, "Client not found")
        return self._to_out(c)

    def update_client(self, email, payload):
        return self._to_out(self.repo.update_client(email, payload))

    def delete_client(self, email):
        self.repo.delete_client(email)
        return {"status": "deleted"}

    async def purchase_ticket(self, email: str, payload: TicketPurchase):
        client = self.repo.get_client(email)
        if not client:
            raise HTTPException(404, "Client not found")

        for _ in range(5):
            ticket_id = uuid.uuid4().hex[:12]

            async with httpx.AsyncClient() as http:
                r = await http.put(
                    f"{EVENT_WS_URL}/tickets/{ticket_id}",
                    json={
                        "EvenimentID": payload.event_id,
                        "PachetID": payload.packet_id,
                        "valid": True,
                    },
                )

            if r.status_code == 204:
                break
            if r.status_code != 409:
                raise HTTPException(500, "Event service error")
        else:
            raise HTTPException(500, "Could not generate unique ticket")

        self.repo.add_ticket(
            email,
            ClientTicket(
                code=ticket_id,
                event_id=payload.event_id,
                packet_id=payload.packet_id,
            )
        )

        return {"ticket_id": ticket_id}
