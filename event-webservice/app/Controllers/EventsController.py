from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Query, status, Security
from fastapi.security import HTTPBearer

from app.Services.EventsService import EventsService
from app.DTO.schemas import EventIn, EventOut, PaginatedResponse
from fastapi import Depends
from app.security.auth import get_current_user

router = APIRouter(prefix="/api/event-manager/events", tags=["events"])

service = EventsService()
security = HTTPBearer()

@router.get(
    "",
    response_model=PaginatedResponse,
    summary="List Events",
)
def list_events(
    page: int = Query(1, ge=1),
    items_per_page: int = Query(10, ge=0),
):
    items, total = EventsService.list_events(page, items_per_page)
    total_pages = 1 if items_per_page == 0 else (total + items_per_page - 1) // items_per_page

    return {
        "items": items,
        "page": page,
        "items_per_page": items_per_page,
        "total_items": total,
        "total_pages": total_pages,
        "_links": {
            "self": {"href": f"/api/event-manager/events?page={page}&items_per_page={items_per_page}"}
        },
    }


@router.post("")
def create_event(
    event: EventIn,
    user=Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create events")

    data = event.dict()
    data["ID_OWNER"] = user["user_id"]
    return service.create_event(data)


@router.get(
    "/{id}",
    response_model=EventOut,
    summary="Get Event",
)
def get_event(id: int):
    event = EventsService.get_event(id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{id}")
def replace_event(
    id: int,
    event: EventIn,
    user = Depends(get_current_user)
):
    existing = service.get_event(id)

    if not existing:
        raise HTTPException(status_code=404, detail="Event not found")

    owner_id = existing["ID_OWNER"] if isinstance(existing, dict) else existing.ID_OWNER

    if user["role"] != "admin" and owner_id != user["user_id"]:
        raise HTTPException(status_code=403, detail="Only admin or owner can update this event")

    data = event.dict()
    data["ID_OWNER"] = owner_id

    return service.replace_event(id, data)


@router.delete(
    "/{id}",
    summary="Delete Event"
)
def delete_event(
    id: int,
    user = Depends(get_current_user)
):
    existing = service.get_event(id)

    if not existing:
        raise HTTPException(status_code=404, detail="Event not found")

    owner_id = (
        existing["ID_OWNER"]
        if isinstance(existing, dict)
        else existing.ID_OWNER
    )

    if user["role"] != "admin" and owner_id != user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="Only admin or owner can delete this event"
        )

    service.delete_event(id)
    return {"status": "deleted"}

@router.get(
    "/{id}/event-packets",
    summary="Event Packets For Event",
)
def event_packets_for_event(id: int):
    return EventsService.event_packets(id)

