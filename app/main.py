from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth_routes, ops, client

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI(
    title="Secure File Sharing API",
    description="Handles secure file uploads and downloads between Ops and Client users",
    version="1.0.0"
)

# Include all routers
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(ops.router, prefix="/ops", tags=["Ops"])
app.include_router(client.router, prefix="/client", tags=["Client"])

# Health check endpoint
@app.get("/")
def root():
    return {"message": "File Share System is Running"}
