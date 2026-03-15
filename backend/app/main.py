"""
Bureaucracy OS — The Operating System for Governance
Main FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import workflows, alerts, analytics, dashboard
from app.core.config import settings

app = FastAPI(
    title="Bureaucracy OS API",
    description="AI-powered workflow intelligence layer for governance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["Workflows"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "Bureaucracy OS",
        "version": "1.0.0",
        "status": "operational",
        "description": "AI-powered workflow intelligence layer for governance",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "services": {"api": True, "database": True, "ai_engine": True}}
