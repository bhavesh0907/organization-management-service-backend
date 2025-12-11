from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class OrgCreateRequest(BaseModel):
    organization_name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)

class OrgGetRequest(BaseModel):
    organization_name: str

class OrgUpdateRequest(BaseModel):
    # New organization name (current org is derived from JWT)
    organization_name: str
    email: EmailStr
    password: str

class OrgDeleteRequest(BaseModel):
    organization_name: str

class OrgResponse(BaseModel):
    id: str
    organization_name: str
    collection_name: str
    admin_email: EmailStr

