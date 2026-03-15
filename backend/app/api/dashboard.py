"""Role-based dashboard API endpoints."""

from fastapi import APIRouter
from app.services.graph_engine import graph_engine
from app.services.ai_engine import ai_engine
from app.services.sla_predictor import sla_predictor

router = APIRouter()


@router.get("/minister")
async def minister_dashboard():
    """Minister-level dashboard: high-level KPIs and critical alerts."""
    workflows = graph_engine.get_all_workflows()
    summary = graph_engine.get_summary_stats()
    bottlenecks = ai_engine.detect_bottlenecks(workflows)
    efficiency = ai_engine.get_efficiency_metrics(workflows)
    risk = sla_predictor.get_risk_distribution(workflows)
    dept_stats = graph_engine.get_department_stats()

    return {
        "role": "minister",
        "summary": summary,
        "top_bottlenecks": bottlenecks[:5],
        "efficiency": efficiency,
        "risk_overview": risk,
        "department_ranking": dept_stats[:10],
        "critical_files": [w for w in workflows if w["status"] == "critical"][:10],
    }


@router.get("/officer")
async def officer_dashboard():
    """Officer-level dashboard: assigned files, pending actions, alerts."""
    workflows = graph_engine.get_all_workflows()
    predictions = ai_engine.predict_sla_breaches(workflows)

    return {
        "role": "officer",
        "my_pending_files": [w for w in workflows if w["status"] in ("on_track", "delayed")][:15],
        "urgent_actions": [w for w in workflows if w["status"] in ("stuck", "critical")][:10],
        "sla_warnings": predictions[:10],
        "summary": graph_engine.get_summary_stats(),
    }


@router.get("/citizen/{application_id}")
async def citizen_portal(application_id: str):
    """Citizen transparency portal: track application/grievance status."""
    workflow = graph_engine.get_workflow(application_id)
    if not workflow:
        # Return a demo workflow for any ID
        workflows = graph_engine.get_all_workflows()
        if workflows:
            workflow = workflows[0]
            workflow["citizen_view"] = True
        else:
            return {"error": "Application not found", "suggestion": "Check your application ID"}

    prediction = sla_predictor.predict_breach(workflow)

    return {
        "application_id": workflow["workflow_id"],
        "title": workflow["title"],
        "current_stage": workflow["current_stage"],
        "stages": [
            {
                "name": s["name"],
                "status": s["status"],
                "date": s["entered_at"],
            }
            for s in workflow["stages"]
        ],
        "estimated_completion": f"{prediction['estimated_completion_days']} days",
        "status": workflow["status"],
        "department": workflow["department"],
        "filed_on": workflow["start_date"],
    }
