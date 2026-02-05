from fastapi import Header, HTTPException, status
from security.idm_client import IDMClient

idm_client = IDMClient()

def get_current_user(authorization: str = Header(None, alias="Authorization")):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    token = authorization.replace("Bearer ", "").strip()

    try:
        response = idm_client.validate_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return {
        "user_id": response.user_id,
        "email": response.email,
        "role": response.role
    }
