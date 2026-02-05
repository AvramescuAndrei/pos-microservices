from fastapi import APIRouter, HTTPException, Query, status, Response

from app.Services.TicketsService import TicketsService
from app.Repositories.TicketsRepository import TicketsRepository
from app.DTO.schemas import TicketIn, TicketOut, PaginatedResponse, TicketPutIn

router = APIRouter(prefix="/api/event-manager/tickets", tags=["tickets"])



@router.get(
    "",
    response_model=PaginatedResponse,
    summary="List Tickets",
)
def list_tickets(
    page: int = Query(1, ge=1),
    items_per_page: int = Query(10, ge=0),
):
    items, total = TicketsService.list_tickets(page, items_per_page)
    total_pages = 1 if items_per_page == 0 else (total + items_per_page - 1) // items_per_page

    return {
        "items": items,
        "page": page,
        "items_per_page": items_per_page,
        "total_items": total,
        "total_pages": total_pages,
        "_links": {
            "self": {"href": f"/api/event-manager/tickets?page={page}&items_per_page={items_per_page}"}
        },
    }


@router.post(
    "",
    response_model=TicketOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create Ticket",
)
def create_ticket(payload: TicketIn):
    if payload.COD is None:
        raise HTTPException(status_code=422, detail="COD is required for POST /tickets")

    ticket = TicketsService.create_ticket(payload.dict())
    return ticket


@router.get(
    "/{cod}",
    response_model=TicketOut,
    summary="Get Ticket",
)
def get_ticket(cod: str):
    ticket = TicketsService.get_ticket(cod)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.delete(
    "/{cod}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Invalidate Ticket",
)
def invalidate_ticket(cod: str):
    ok = TicketsService.invalidate_ticket(cod)
    if not ok:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return Response(status_code=204)

@router.put(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Create Ticket via PUT (id comes from path)",
)
def create_ticket_via_put(ticket_id: str, payload: TicketPutIn):
    existing = TicketsRepository.get_ticket(ticket_id)
    if existing is not None:
        raise HTTPException(status_code=409, detail="Ticket already exists")

    TicketsRepository.create_ticket_with_code(
        code=ticket_id,
        event_id=payload.EvenimentID,
        packet_id=payload.PachetID,
        valid=payload.valid,
    )

    return Response(status_code=204)
