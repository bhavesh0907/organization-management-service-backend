from fastapi import APIRouter, Depends
from ..schemas.auth_schemas import TokenResponse, AdminLoginRequest
from ..services.auth_service import AuthService

router = APIRouter(
    prefix="/admin",           # combined with /auth -> /auth/admin/...
    tags=["Authentication"],
)


def get_auth_service():
    return AuthService()


@router.post("/login", response_model=TokenResponse, summary="Admin Login")
def admin_login(
    login_data: AdminLoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    POST /auth/admin/login

    Input:
    - email
    - password

    Returns:
    - JWT access token (bearer)
    """
    token = auth_service.admin_login(
        email=login_data.email,
        password=login_data.password
    )
    return TokenResponse(access_token=token)

