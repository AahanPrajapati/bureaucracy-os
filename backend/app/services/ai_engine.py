"""
AI Analytics Engine — Layer 3 (The Intelligence)
Detects anomalies, identifies bottlenecks, and generates recommendations.
"""

from typing import List, Dict
import random


class AIAnalyticsEngine:
    """
    In production, this uses:
    - Claude API for natural language root cause analysis
    - Scikit-learn for delay prediction models
    - PM4Py for process mining and deviation detection
    
    For the prototype, we simulate AI-generated insights.
    """

    BOTTLENECK_TEMPLATES = [
        {
            "root_cause": "Sequential multi-officer sign-off causing cascading delays",
            "recommendation": "Parallelize verification — officers can review simultaneously since checks are independent",
            "savings_days": 11,
        },
        {
            "root_cause": "Single-point-of-failure: one officer handles all approvals for this category",
            "recommendation": "Distribute workload across 2-3 officers with rotating assignment",
            "savings_days": 8,
        },
        {
            "root_cause": "Missing documentation causes repeated back-and-forth between departments",
            "recommendation": "Implement pre-submission checklist with automated document validation",
            "savings_days": 14,
        },
        {
            "root_cause": "Handoff gap: no clear ownership during department-to-department transfer",
            "recommendation": "Assign transition officer role with 24-hour pickup SLA at handoff points",
            "savings_days": 6,
        },
        {
            "root_cause": "Approval authority on extended leave with no designated alternate",
            "recommendation": "Mandate delegation-of-authority protocol with automatic alternate routing",
            "savings_days": 9,
        },
    ]

    def detect_bottlenecks(self, workflows: List[Dict]) -> List[Dict]:
        """Analyze workflows to detect bottlenecks and generate AI recommendations."""
        stuck_workflows = [w for w in workflows if w["status"] in ("stuck", "delayed", "critical")]
        
        # Group by department to find systemic issues
        dept_issues = {}
        for w in stuck_workflows:
            dept = w["department"]
            if dept not in dept_issues:
                dept_issues[dept] = []
            dept_issues[dept].append(w)

        bottlenecks = []
        for dept, dept_workflows in dept_issues.items():
            if len(dept_workflows) >= 1:
                template = random.choice(self.BOTTLENECK_TEMPLATES)
                bottlenecks.append({
                    "bottleneck_id": f"BN-{random.randint(1000, 9999)}",
                    "department": dept,
                    "stage": dept_workflows[0]["current_stage"],
                    "files_affected": len(dept_workflows),
                    "avg_delay_days": round(sum(w["days_elapsed"] for w in dept_workflows) / len(dept_workflows), 1),
                    "root_cause": template["root_cause"],
                    "ai_recommendation": template["recommendation"],
                    "potential_savings_days": template["savings_days"],
                    "confidence": round(random.uniform(0.72, 0.95), 2),
                    "similar_pending_files": random.randint(5, 30),
                    "severity": "critical" if len(dept_workflows) >= 3 else "warning",
                })

        return sorted(bottlenecks, key=lambda x: x["files_affected"], reverse=True)

    def predict_sla_breaches(self, workflows: List[Dict]) -> List[Dict]:
        """Predict which workflows will breach SLA in the next 48-72 hours."""
        predictions = []
        for w in workflows:
            if w["status"] in ("on_track", "delayed") and 0 < w["sla_remaining"] <= 5:
                breach_probability = round(1 - (w["sla_remaining"] / w["sla_days"]), 2)
                predictions.append({
                    "workflow_id": w["workflow_id"],
                    "title": w["title"],
                    "department": w["department"],
                    "current_stage": w["current_stage"],
                    "sla_remaining_days": w["sla_remaining"],
                    "breach_probability": min(breach_probability, 0.97),
                    "predicted_breach_in": f"{w['sla_remaining']} days",
                    "recommended_action": f"Escalate to department head — file has been at '{w['current_stage']}' for {w['days_elapsed'] - (w['sla_days'] - w['sla_remaining'])} days",
                })

        return sorted(predictions, key=lambda x: x["breach_probability"], reverse=True)

    def get_efficiency_metrics(self, workflows: List[Dict]) -> Dict:
        """Calculate system-wide efficiency metrics."""
        total = len(workflows)
        if total == 0:
            return {}

        completed = [w for w in workflows if w["status"] == "completed"]
        avg_completion = sum(w["days_elapsed"] for w in completed) / max(len(completed), 1)

        return {
            "total_active_files": total - len(completed),
            "files_completed_this_month": len(completed),
            "avg_completion_days": round(avg_completion, 1),
            "bottleneck_departments": len(set(w["department"] for w in workflows if w["status"] in ("stuck", "critical"))),
            "handoff_delay_percentage": round(random.uniform(55, 72), 1),
            "ai_interventions_this_week": random.randint(15, 45),
            "estimated_savings_crore": round(random.uniform(12, 85), 1),
            "sla_compliance_trend": [
                {"month": "Oct 2024", "rate": 62.3},
                {"month": "Nov 2024", "rate": 68.1},
                {"month": "Dec 2024", "rate": 71.5},
                {"month": "Jan 2025", "rate": 74.8},
                {"month": "Feb 2025", "rate": 79.2},
                {"month": "Mar 2025", "rate": 83.6},
            ],
        }


# Singleton instance
ai_engine = AIAnalyticsEngine()
