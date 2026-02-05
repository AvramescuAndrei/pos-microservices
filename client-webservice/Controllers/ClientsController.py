from typing import List
from fastapi import APIRouter, Path, Depends, HTTPException
from security.auth import get_current_user

from DTO.schemas import ClientCreate, ClientOut, ClientUpdate, TicketPurchase
from Services.ClientsService import ClientsService

router = APIRouter(
    prefix="/api/clients",
    tags=["clients"]
)

service = ClientsService()


@router.post("", response_model=ClientOut, status_code=201)
def create_client(
    payload: ClientCreate,
    user = Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can create clients"
        )

    return service.create_client(payload)

@router.get("", response_model=List[ClientOut])
def list_clients(user = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can list clients"
        )

    return service.get_clients()


@router.get("/{email}", response_model=ClientOut)
def get_client(
    email: str = Path(...),
    user = Depends(get_current_user)
):
    if user["role"] != "admin" and user["email"] != email:
        raise HTTPException(
            status_code=403,
            detail="Only admin or owner can view this client"
        )

    return service.get_client(email)


from fastapi import Depends, HTTPException
from security.auth import get_current_user

@router.patch("/{email}", response_model=ClientOut)
def update_client(
    email: str,
    payload: ClientUpdate,
    user = Depends(get_current_user)
):
    if user["email"] != email:
        raise HTTPException(
            status_code=403,
            detail="Only owner can update this client"
        )

    return service.update_client(email, payload)



@router.delete("/{email}")
def delete_client(
    email: str,
    user = Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete clients"
        )

    return service.delete_client(email)


@router.post("/{email}/tickets", summary="Buy ticket (client -> event webservice)")
async def buy_ticket(email: str, payload: TicketPurchase):
    return await service.purchase_ticket(email, payload)
