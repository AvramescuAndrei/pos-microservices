from fastapi import APIRouter, HTTPException, Query, status

from app.Services.PacketsService import PacketsService
from app.DTO.schemas import EventPacketIn, EventPacketOut, PaginatedResponse

router = APIRouter(prefix="/api/event-manager/event-packets", tags=["event-packets"])



@router.get(
    "",
    response_model=PaginatedResponse,
    summary="List Packets",
)
def list_packets(
    page: int = Query(1, ge=1),
    items_per_page: int = Query(10, ge=0),
):
    items, total = PacketsService.list_packets(page, items_per_page)
    total_pages = 1 if items_per_page == 0 else (total + items_per_page - 1) // items_per_page

    return {
        "items": items,
        "page": page,
        "items_per_page": items_per_page,
        "total_items": total,
        "total_pages": total_pages,
        "_links": {
            "self": {"href": f"/api/event-manager/event-packets?page={page}&items_per_page={items_per_page}"}
        },
    }


@router.post(
    "",
    response_model=EventPacketOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create Packet",
)
def create_packet(payload: EventPacketIn):
    packet = PacketsService.create_packet(payload.dict())
    return packet


@router.get(
    "/{id}",
    response_model=EventPacketOut,
    summary="Get Packet",
)
def get_packet(id: int):
    packet = PacketsService.get_packet(id)
    if packet is None:
        raise HTTPException(status_code=404, detail="Packet not found")
    return packet


@router.put(
    "/{id}",
    response_model=EventPacketOut,
    summary="Replace Packet",
)
def replace_packet(id: int, payload: EventPacketIn):
    packet = PacketsService.replace_packet(id, payload.dict())
    if packet is None:
        raise HTTPException(status_code=404, detail="Packet not found")
    return packet


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Packet",
)
def delete_packet(id: int):
    ok = PacketsService.delete_packet(id)
    if not ok:
        raise HTTPException(status_code=404, detail="Packet not found")


@router.get(
    "/{id}/events",
    summary="Events in packet",
)
def events_in_packet(id: int):
    return PacketsService.events_in_packet(id)
