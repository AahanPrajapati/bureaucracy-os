"""Alert management API endpoints."""

from fastapi import APIRouter, Query
from typing import Optional
from app.services.graph_engine import graph_engine
from app.services.ai_engine import ai_engine

router = APIRouter()


@router.get("/")
async def get_active_alerts(
    severity: Optional[str] = Query(None, description="Filter: info, warning, critical"),
    department: Optional[str] = None,
):
    """Get all active SLA and bottleneck alerts."""
    workflows = graph_engine.get_all_workflows()
    
    # SLA breach predictions
    sla_alerts = ai_engine.predict_sla_breaches(workflows)
    
    # Bottleneck alerts
    bottleneck_alerts = ai_engine.detect_bottlenecks(workflows)

    all_alerts = []
    for s in sla_alerts[:10]:
        all_alerts.append({
            "type": "sla_breach_predicted",
            "severity": "critical" if s["breach_probability"] > 0.8 else "warning",
            **s,
        })

    for b in bottleneck_alerts[:10]:
        all_alerts.append({
            "type": "bottleneck_detected",
            **b,
        })

    if severity:
        all_alerts = [a for a in all_alerts if a.get("severity") == severity]
    if department:
        all_alerts = [a for a in all_alerts if a.get("department") == department]

    return {"total": len(all_alerts), "alerts": all_alerts}
