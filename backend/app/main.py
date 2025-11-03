"""
Main FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import health, auth, users, client, coach, admin, feedback, bookings, chat
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for Vibe Fitness Coaching Platform",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configure CORS
allowed_origins = list(settings.ALLOWED_ORIGINS)

# Add ngrok URLs if configured
if settings.NGROK_FRONTEND_URL:
    allowed_origins.append(settings.NGROK_FRONTEND_URL)
if settings.NGROK_BACKEND_URL:
    allowed_origins.append(settings.NGROK_BACKEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(client.router, prefix="/api/v1/client", tags=["client"])
app.include_router(coach.router, prefix="/api/v1/coach", tags=["coach"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(feedback.router, prefix="/api/v1/feedback", tags=["feedback"])
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["bookings"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Vibe Fitness Platform API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
    }
