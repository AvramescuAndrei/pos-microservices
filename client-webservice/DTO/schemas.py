from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, root_validator


class ClientBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_name_public: bool = False
    social_links: Optional[Dict[str, Any]] = None
    is_social_public: bool = False


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_name_public: Optional[bool] = None
    social_links: Optional[Dict[str, Any]] = None
    is_social_public: Optional[bool] = None


class ClientTicket(BaseModel):
    code: str
    event_id: Optional[int] = None
    packet_id: Optional[int] = None


class ClientOut(ClientBase):
    tickets: List[ClientTicket] = []
    _links: Dict[str, Dict[str, str]]


class TicketPurchase(BaseModel):
    event_id: Optional[int] = None
    packet_id: Optional[int] = None

    @root_validator
    def exactly_one(cls, values):
        e, p = values.get("event_id"), values.get("packet_id")
        if (e is None and p is None) or (e is not None and p is not None):
            raise ValueError("Provide EXACTLY one of event_id or packet_id")
        return values
