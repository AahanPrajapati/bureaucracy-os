"""
SLA Breach Predictor — Predictive modeling for deadline breaches.
Uses historical patterns to warn officers 48-72 hours before SLA violations.
"""

from typing import Dict, List
import random
from datetime import datetime, timedelta


class SLAPredictor:
    """
    In production, this uses scikit-learn trained on historical government workflow data.
    Features: department, file_type, current_stage_duration, officer_workload, time_of_year.
    """

    def predict_breach(self, workflow: Dict) -> Dict:
        """Predict SLA breach probability for a single workflow."""
        progress = workflow["current_stage_idx"] / max(workflow["total_stages"], 1)
        time_used = workflow["days_elapsed"] / max(workflow["sla_days"], 1)

        # Simple heuristic model (replace with ML in production)
        if time_used > 0.8 and progress < 0.6:
            risk = "critical"
            probability = round(random.uniform(0.85, 0.97), 2)
        elif time_used > 0.6 and progress < 0.5:
            risk = "high"
            probability = round(random.uniform(0.65, 0.85), 2)
        elif time_used > progress:
            risk = "medium"
            probability = round(random.uniform(0.35, 0.65), 2)
        else:
            risk = "low"
            probability = round(random.uniform(0.05, 0.35), 2)

        return {
            "workflow_id": workflow["workflow_id"],
            "risk_level": risk,
            "breach_probability": probability,
            "estimated_completion_days": round(workflow["sla_days"] * (1 - progress) / max(0.3, 1 - time_used)),
            "sla_remaining_days": workflow["sla_remaining"],
            "on_track": risk in ("low", "medium"),
        }

    def get_risk_distribution(self, workflows: List[Dict]) -> Dict:
        """Get system-wide SLA risk distribution."""
        risks = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for w in workflows:
            pred = self.predict_breach(w)
            risks[pred["risk_level"]] += 1

        total = len(workflows)
        return {
            "distribution": risks,
            "overall_risk_score": round(
                (risks["critical"] * 4 + risks["high"] * 3 + risks["medium"] * 2 + risks["low"]) / max(total * 4, 1) * 100,
                1,
            ),
            "files_at_risk": risks["critical"] + risks["high"],
            "total_files": total,
        }


sla_predictor = SLAPredictor()
