# Organization Management Service  
Backend Assignment for **The Wedding Company**

This project implements a complete backend service for managing organizations and administrators.  
It is designed with clean, modular architecture, adhering to production-grade backend standards.

This README includes a dedicated **Reviewer Guide** for The Wedding Company’s hiring team.

---

# 1. Reviewer Guide (For The Wedding Company)

Thank you for reviewing this submission.  
To help you test the backend quickly, here is everything you need:

### **A. GitHub Repository**
All project files are available here:

https://github.com/bhavesh0907/organization-management-service-backend

bash
Copy code

### **B. Quick Run Instructions (2 Minutes)**

1. Clone repository  
   ```bash
   git clone git@github.com:bhavesh0907/organization-management-service-backend.git
   cd organization-management-service-backend
Create virtual environment

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install dependencies

bash
Copy code
pip install -r requirements.txt
Start MongoDB (macOS example)

bash
Copy code
brew services start mongodb-community@7.0
Run backend

bash
Copy code
uvicorn app.main:app --reload
C. API Documentation
Swagger UI:

arduino
Copy code
http://127.0.0.1:8000/docs
ReDoc:

arduino
Copy code
http://127.0.0.1:8000/redoc
D. Postman Collection
Included in repository:

pgsql
Copy code
organization-management-collection.json
Import into Postman → Ready-to-run requests included.

2. Overview
The Organization Management Service provides:

Secure admin authentication (JWT)

Organization creation

Dynamic organization-level collections in MongoDB

Update & delete operations with validation

Auto-migration of collection names on organization updates

3. Features
FastAPI-based modern backend

JWT authentication

Bcrypt password hashing

Organization-specific collections

Modular service-layer architecture

Fully documented API (Swagger & Postman)

Clean code structure suitable for scaling

4. Architecture
mermaid
Copy code
flowchart LR
    Client[Client / Postman / Swagger UI] -->|HTTP| API[FastAPI Application]

    subgraph FastAPI App
        Routes[Routes]
        Services[Business Services]
        Schemas[Pydantic Schemas]
        Utils[Security Utils]
        DB[MongoDB Layer]
    end

    API --> Routes
    Routes --> Services
    Services --> DB
    Services --> Utils

    DB -->|PyMongo| MongoDB[(MongoDB Database)]
5. Project Structure
pgsql
Copy code
org-management-service/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   └── utils/
├── organization-management-collection.json
├── requirements.txt
└── README.md
6. API Reference
Health Check
sql
Copy code
GET /
Response

json
Copy code
{
  "status": "ok",
  "service": "Organization Management Service",
  "version": "1.0.0"
}
Create Organization
bash
Copy code
POST /org/create
Request

json
Copy code
{
  "organization_name": "Acme Corp",
  "email": "admin@acme.com",
  "password": "StrongPass123"
}
Response

json
Copy code
{
  "id": "693b1333884d2ef6125c875b",
  "organization_name": "Acme Corp",
  "collection_name": "org_acme_corp",
  "admin_email": "admin@acme.com"
}
Admin Login
pgsql
Copy code
POST /auth/admin/login
Request

json
Copy code
{
  "email": "admin@acme.com",
  "password": "StrongPass123"
}
Response

json
Copy code
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
Get Organization
sql
Copy code
GET /org/get?organization_name=Acme Corp
Update Organization
(Protected endpoint)

bash
Copy code
PUT /org/update
Headers

makefile
Copy code
Authorization: Bearer <JWT_TOKEN>
Delete Organization
(Protected endpoint)

sql
Copy code
DELETE /org/delete
7. Postman Collection
A complete Postman collection is included:

pgsql
Copy code
organization-management-collection.json
Import → Run all requests directly.

8. Screenshots
To keep the README clean, screenshots are stored in a folder named docs/.

Once added, they will render automatically:

markdown
Copy code
## Swagger – Organization Endpoints
![Swagger Organization Endpoints](docs/swagger-organization-endpoints.png)

## Swagger – Auth Modal
![Swagger OAuth2 Auth](docs/swagger-oauth2-authorization.png)

## Full API Overview
![Swagger API Overview](docs/swagger-api-overview.png)

## Root Endpoint
![Root Healthcheck](docs/root-healthcheck.png)
9. Future Improvements
Add role-based access

Add organization analytics

Dockerize the service

Add unit tests with pytest

Add rate limiting

Add CI/CD pipeline

10. Author
Bhavesh Mishra
Backend Assignment Submission for The Wedding Company
Python | FastAPI | MongoDB | JWT Authentication

yaml
Copy code

---

# ✅ Next Step for You

### Create `docs/` folder and add screenshots:

mkdir docs

markdown
Copy code

Move your screenshot PNG files inside it:
- swagger-organization-endpoints.png  
- swagger-oauth2-authorization.png  
- swagger-api-overview.png  
- root-healthcheck.png  

### Then push changes:

```bash
git add docs/*.png README.md
git commit -m "Added final README and screenshots"
git push
