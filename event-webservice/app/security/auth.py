from fastapi import Header, HTTPException, status
from app.security.idm_client import IDMClient

idm_client = IDMClient()

def get_current_user(authorization: str = Header(None, alias="Authorization")):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    token = authorization.replace("Bearer ", "")

    response = idm_client.validate_token(token)

    if not response.valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response.message
        )

    return {"user_id": response.user_id, "role": response.role, "email": response.email}