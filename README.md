# Organization Management Service

## Overview

This project is a backend service for managing organizations in a multi-tenant way. It was implemented as part of a backend assignment.

Core features:

- Create organization with an admin user
- Admin login with JWT authentication
- Get organization details by name
- Update organization (name + admin email + admin password)
- Delete organization (only by the respective admin)
- Dynamic MongoDB collections per organization

---

## Tech Stack

- Python 3.10
- FastAPI
- MongoDB (local, via Homebrew)
- PyJWT (JWT auth)
- passlib + bcrypt (password hashing)
- Uvicorn (development server)
- Postman (API testing)

---

## Project Structure

```text
org-management-service/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── models/
│   │   ├── organization.py
│   │   └── admin.py
│   ├── schemas/
│   │   ├── org_schemas.py
│   │   └── auth_schemas.py
│   ├── services/
│   │   ├── org_service.py
│   │   └── auth_service.py
│   ├── routes/
│   │   ├── org_routes.py
│   │   ├── auth_routes.py
│   │   └── deps.py
│   └── utils/
│       ├── security.py
│       └── common.py
├── requirements.txt
├── .env
├── README.md
└── organization-management-collection.json   # Postman collection
