from fastapi import FastAPI

from .routes import org_routes, auth_routes

app = FastAPI(
    title="Organization Management Service",
    version="1.0.0",
    description="Backend service for organization management"
)


@app.get("/", tags=["default"])
def root():
    """
    Simple health check / root endpoint.
    """
    return {
        "status": "ok",
        "service": "Organization Management Service",
        "version": "1.0.0",
    }


# Authentication routes
# Final path: /auth/admin/login
app.include_router(auth_routes.router, prefix="/auth")

# Organization routes
# Final paths:
# - /org/create
# - /org/get
# - /org/update
# - /org/delete
app.include_router(org_routes.router, prefix="/org")

