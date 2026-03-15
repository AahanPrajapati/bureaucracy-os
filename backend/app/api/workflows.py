"""Workflow tracking API endpoints."""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from app.services.graph_engine import graph_engine

router = APIRouter()


@router.get("/")
async def list_workflows(
    status: Optional[str] = Query(None, description="Filter by status: on_track, delayed, stuck, critical, completed"),
    department: Optional[str] = Query(None, description="Filter by department name"),
    limit: int = Query(50, ge=1, le=200),
):
    """List all tracked workflows with optional filters."""
    workflows = graph_engine.get_all_workflows(status=status, department=department)
    return {"total": len(workflows), "workflows": workflows[:limit]}


@router.get("/summary")
async def workflow_summary():
    """Get aggregate workflow statistics."""
    return graph_engine.get_summary_stats()


@router.get("/departments")
async def department_stats():
    """Get per-department workflow statistics and bottleneck scores."""
    return {"departments": graph_engine.get_department_stats()}


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get detailed workflow information including full stage history."""
    workflow = graph_engine.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
    return workflow


@router.post("/ingest")
async def ingest_event(event: dict):
    """Ingest a new workflow event from external systems (e-Office, CMS, etc.)."""
    # In production, this publishes to Kafka and updates Neo4j
    return {
        "status": "accepted",
        "message": "Event ingested and queued for processing",
        "event": event,
    }
