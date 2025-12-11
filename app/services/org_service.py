from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status

from ..db import db, organizations_collection, admins_collection
from ..models.organization import Organization
from ..models.admin import AdminUser
from ..utils.common import org_name_to_collection_name
from ..utils.security import hash_password


class OrgService:
    def __init__(self):
        self.db = db
        self.orgs = organizations_collection
        self.admins = admins_collection

    def _ensure_org_not_exists(self, name: str):
        if self.orgs.find_one({"name": name}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization with this name already exists.",
            )

    def _get_org_by_name(self, name: str) -> dict:
        org = self.orgs.find_one({"name": name})
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found.",
            )
        return org

    def create_organization(self, organization_name: str, email: str, password: str) -> dict:
        self._ensure_org_not_exists(organization_name)

        collection_name = org_name_to_collection_name(organization_name)
        admin_id = ObjectId()

        org = Organization(
            name=organization_name,
            collection_name=collection_name,
            admin_id=admin_id,
        )

        admin_user = AdminUser(
            _id=admin_id,
            email=email,
            password_hash=hash_password(password),
            org_id=org.id,
        )

        # Insert in master DB
        self.orgs.insert_one(org.to_document())
        self.admins.insert_one(admin_user.to_document())

        # Create dynamic collection for org
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)

        return {
            "id": str(org.id),
            "organization_name": org.name,
            "collection_name": org.collection_name,
            "admin_email": admin_user.email,
        }

    def get_organization_by_name(self, organization_name: str) -> dict:
        org = self._get_org_by_name(organization_name)
        admin = self.admins.find_one({"_id": org["admin_id"]})
        return {
            "id": str(org["_id"]),
            "organization_name": org["name"],
            "collection_name": org["collection_name"],
            "admin_email": admin["email"] if admin else None,
        }

    def update_organization_for_admin(
        self,
        current_org_id: ObjectId,
        new_org_name: str,
        new_email: str,
        new_password: str,
    ) -> dict:
        """
        Assumption:
        - Admin is authenticated; current org ID is from JWT.
        - new_org_name must be unique.
        - We treat this as a "rename org + rotate admin creds".
        """
        current_org = self.orgs.find_one({"_id": current_org_id})
        if not current_org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Current organization not found.",
            )

        if current_org["name"] != new_org_name:
            self._ensure_org_not_exists(new_org_name)

        old_collection_name = current_org["collection_name"]
        new_collection_name = org_name_to_collection_name(new_org_name)

        # Create new collection and migrate data
        old_collection = self.db[old_collection_name]
        new_collection = self.db[new_collection_name]

        if new_collection_name not in self.db.list_collection_names():
            self.db.create_collection(new_collection_name)

        # Simple full copy (could be optimized / chunked)
        docs = list(old_collection.find({}))
        if docs:
            for d in docs:
                d.pop("_id", None)
            new_collection.insert_many(docs)

        # Optionally drop old collection
        if old_collection_name != new_collection_name:
            self.db.drop_collection(old_collection_name)

        # Update org document
        self.orgs.update_one(
            {"_id": current_org_id},
            {
                "$set": {
                    "name": new_org_name,
                    "collection_name": new_collection_name,
                }
            },
        )

        # Update admin user credentials
        self.admins.update_one(
            {"org_id": current_org_id},
            {
                "$set": {
                    "email": new_email,
                    "password_hash": hash_password(new_password),
                }
            },
        )

        admin = self.admins.find_one({"org_id": current_org_id})

        return {
            "id": str(current_org_id),
            "organization_name": new_org_name,
            "collection_name": new_collection_name,
            "admin_email": admin["email"] if admin else None,
        }

    def delete_organization(self, current_org_id: ObjectId, organization_name: str):
        """
        Only allow deletion by authenticated admin.
        Cross-check org name to avoid accidental delete.
        """
        org = self.orgs.find_one({"_id": current_org_id})
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found.",
            )

        if org["name"] != organization_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization name mismatch.",
            )

        # Drop dynamic collection
        collection_name = org["collection_name"]
        self.db.drop_collection(collection_name)

        # Delete admin users
        self.admins.delete_many({"org_id": current_org_id})

        # Delete organization
        self.orgs.delete_one({"_id": current_org_id})

        return {"detail": "Organization deleted successfully."}

