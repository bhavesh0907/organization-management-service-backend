from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..utils.security import decode_token
from ..services.auth_service import AuthService

# This must match the actual login URL: /auth/admin/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/admin/login")


def get_auth_service():
    return AuthService()


def get_current_admin_and_org(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Dependency that:
    - Decodes JWT
    - Validates token
    - Returns (admin_id, org_id) as ObjectId pair
    """
    try:
        payload = decode_token(token)
        admin_id, org_id = auth_service.parse_admin_from_token_payload(payload)
        return admin_id, org_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

