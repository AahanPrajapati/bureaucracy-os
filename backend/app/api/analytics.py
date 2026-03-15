"""AI Analytics API endpoints."""

from fastapi import APIRouter
from app.services.graph_engine import graph_engine
from app.services.ai_engine import ai_engine
from app.services.sla_predictor import sla_predictor

router = APIRouter()


@router.get("/bottlenecks")
async def get_bottlenecks():
    """AI-detected bottlenecks with root cause analysis and recommendations."""
    workflows = graph_engine.get_all_workflows()
    bottlenecks = ai_engine.detect_bottlenecks(workflows)
    return {"total": len(bottlenecks), "bottlenecks": bottlenecks}


@router.get("/predictions")
async def get_sla_predictions():
    """Predict upcoming SLA breaches (48-72 hour window)."""
    workflows = graph_engine.get_all_workflows()
    predictions = ai_engine.predict_sla_breaches(workflows)
    return {"total": len(predictions), "predictions": predictions}


@router.get("/efficiency")
async def get_efficiency_metrics():
    """System-wide governance efficiency metrics."""
    workflows = graph_engine.get_all_workflows()
    return ai_engine.get_efficiency_metrics(workflows)


@router.get("/risk-distribution")
async def get_risk_distribution():
    """SLA risk distribution across all active workflows."""
    workflows = graph_engine.get_all_workflows()
    return sla_predictor.get_risk_distribution(workflows)


@router.get("/workflow/{workflow_id}/analysis")
async def analyze_workflow(workflow_id: str):
    """Deep AI analysis of a specific workflow."""
    workflow = graph_engine.get_workflow(workflow_id)
    if not workflow:
        return {"error": "Workflow not found"}

    prediction = sla_predictor.predict_breach(workflow)

    return {
        "workflow": workflow,
        "sla_prediction": prediction,
        "ai_analysis": {
            "current_status_assessment": f"File is at '{workflow['current_stage']}' stage — "
            f"{'on track' if prediction['on_track'] else 'at risk of SLA breach'}",
            "delay_factors": [
                "Sequential approval chain creating cascading wait times",
                "Officer workload imbalance in current department",
            ]
            if not prediction["on_track"]
            else [],
            "recommendation": "Escalate to department head for expedited processing"
            if prediction["risk_level"] in ("high", "critical")
            else "No action needed — workflow progressing normally",
        },
    }
