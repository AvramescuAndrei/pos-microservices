from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, root_validator


class EventIn(BaseModel):
    nume: str
    locatie: str
    descriere: Optional[str] = None
    numarLocuri: int = Field(gt=0)


class EventOut(EventIn):
    ID: int
    _links: Dict[str, Dict[str, str]]


class EventPacketIn(BaseModel):
    nume: str
    descriere: Optional[str] = None
    numarLocuri: Optional[int] = Field(default=None, gt=0)

class TicketPutIn(BaseModel):
    EvenimentID: Optional[int] = None
    PachetID: Optional[int] = None
    valid: bool = True

    @root_validator
    def validate_exactly_one(cls, values):
        e = values.get("EvenimentID")
        p = values.get("PachetID")

        if (e is None and p is None) or (e is not None and p is not None):
            raise ValueError("Provide EXACTLY one of EvenimentID or PachetID")

        return values
    
class EventPacketOut(EventPacketIn):
    ID: int
    _links: Dict[str, Dict[str, str]]


class TicketIn(BaseModel):
    COD: str
    EvenimentID: Optional[int] = None
    PachetID: Optional[int] = None
    valid: bool = True


class TicketOut(BaseModel):
    COD: str
    EvenimentID: Optional[int]
    PachetID: Optional[int]
    valid: bool
    _links: Dict[str, Dict[str, str]]


class PaginatedResponse(BaseModel):
    items: List[Dict[str, Any]]
    page: int
    items_per_page: int
    total_items: int
    total_pages: int
    _links: Dict[str, Dict[str, str]]
