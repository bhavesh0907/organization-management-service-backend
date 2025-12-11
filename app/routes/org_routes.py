from fastapi import APIRouter, Depends

from ..schemas.org_schemas import (
    OrgCreateRequest,
    OrgGetRequest,
    OrgUpdateRequest,
    OrgDeleteRequest,
    OrgResponse,
)
from ..services.org_service import OrgService
from .deps import get_current_admin_and_org

router = APIRouter(
    tags=["Organization"],   # no prefix here; prefix is added in main.py
)


def get_org_service():
    return OrgService()


@router.post("/create", response_model=OrgResponse, summary="Create Org")
def create_org(
    body: OrgCreateRequest,
    org_service: OrgService = Depends(get_org_service),
):
    """
    POST /org/create
    """
    result = org_service.create_organization(
        organization_name=body.organization_name,
        email=body.email,
        password=body.password,
    )
    return OrgResponse(**result)


@router.get("/get", response_model=OrgResponse, summary="Get Org")
def get_org(
    organization_name: str,
    org_service: OrgService = Depends(get_org_service),
):
    """
    GET /org/get?organization_name=...
    """
    result = org_service.get_organization_by_name(organization_name)
    return OrgResponse(**result)


@router.put("/update", response_model=OrgResponse, summary="Update Org")
def update_org(
    body: OrgUpdateRequest,
    org_service: OrgService = Depends(get_org_service),
    current=Depends(get_current_admin_and_org),
):
    """
    PUT /org/update
    Auth required (Bearer token).
    Uses org_id from JWT and new fields from body.
    """
    _, org_id = current
    result = org_service.update_organization_for_admin(
        current_org_id=org_id,
        new_org_name=body.organization_name,
        new_email=body.email,
        new_password=body.password,
    )
    return OrgResponse(**result)


@router.delete("/delete", summary="Delete Org")
def delete_org(
    body: OrgDeleteRequest,
    org_service: OrgService = Depends(get_org_service),
    current=Depends(get_current_admin_and_org),
):
    """
    DELETE /org/delete
    Auth required (Bearer token).
    Only respective admin can delete.
    """
    _, org_id = current
    result = org_service.delete_organization(
        current_org_id=org_id,
        organization_name=body.organization_name,
    )
    return result

