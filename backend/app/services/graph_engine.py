"""
Workflow Graph Engine — Layer 2 (The Brain)
Manages the live workflow graph using Neo4j.
Models department-file-officer relationships as a traversable graph.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random


class WorkflowGraphEngine:
    """
    In production, this connects to Neo4j to maintain a live directed graph where:
    - Nodes represent files, departments, and officers
    - Edges represent approvals, transfers, and handoffs
    
    For the prototype, we use in-memory simulation.
    """

    def __init__(self):
        self._workflows = self._generate_sample_workflows()

    def _generate_sample_workflows(self) -> List[Dict]:
        """Generate realistic sample workflow data for demonstration."""
        departments = [
            "Public Works Dept", "Finance Dept", "Urban Development",
            "Revenue Dept", "Health Dept", "Education Dept",
            "Transport Dept", "Agriculture Dept", "IT Dept",
            "Home Affairs", "Environment Dept", "Water Resources"
        ]

        stages_templates = {
            "infrastructure": [
                "File Submission", "Technical Review", "Dept Head Approval",
                "Finance Review", "Legal Sign-off", "Final Approval"
            ],
            "grievance": [
                "Complaint Filed", "Initial Assessment", "Department Routing",
                "Investigation", "Resolution Draft", "Closure"
            ],
            "permit": [
                "Application Received", "Document Verification", "Site Inspection",
                "Committee Review", "Approval/Rejection"
            ],
        }

        workflows = []
        statuses = ["on_track", "delayed", "stuck", "completed", "critical"]

        for i in range(50):
            wf_type = random.choice(list(stages_templates.keys()))
            stages = stages_templates[wf_type]
            dept = random.choice(departments)
            current_stage_idx = random.randint(0, len(stages) - 1)
            status = random.choice(statuses)

            start_date = datetime.now() - timedelta(days=random.randint(1, 90))
            stage_data = []
            for j, stage_name in enumerate(stages):
                entered = start_date + timedelta(days=j * random.randint(2, 8))
                completed = entered + timedelta(days=random.randint(1, 14)) if j < current_stage_idx else None
                stage_data.append({
                    "stage_id": f"STG-{i:03d}-{j:02d}",
                    "name": stage_name,
                    "entered_at": entered.isoformat(),
                    "completed_at": completed.isoformat() if completed else None,
                    "expected_days": random.randint(2, 7),
                    "actual_days": (completed - entered).days if completed else (datetime.now() - entered).days,
                    "status": "completed" if j < current_stage_idx else ("active" if j == current_stage_idx else "pending"),
                    "officer": f"Officer-{random.randint(100, 999)}",
                })

            days_elapsed = (datetime.now() - start_date).days
            sla_days = random.randint(15, 60)

            workflows.append({
                "workflow_id": f"WF-2024-{i+1:04d}",
                "file_number": f"DL-2024-{random.randint(1, 999):03d}",
                "title": f"{'Road Project' if wf_type == 'infrastructure' else 'Citizen Grievance' if wf_type == 'grievance' else 'Building Permit'} #{i+1}",
                "type": wf_type,
                "department": dept,
                "status": status,
                "priority": random.choice(["low", "medium", "high", "critical"]),
                "current_stage": stages[current_stage_idx],
                "current_stage_idx": current_stage_idx,
                "total_stages": len(stages),
                "stages": stage_data,
                "start_date": start_date.isoformat(),
                "sla_days": sla_days,
                "days_elapsed": days_elapsed,
                "sla_remaining": max(0, sla_days - days_elapsed),
                "initiated_by": f"Dept-{random.randint(1, 20):02d}",
                "tags": random.sample(["urgent", "VIP", "RTI", "court-ordered", "PMO-flagged", "public-interest"], k=random.randint(0, 2)),
            })

        return workflows

    def get_all_workflows(self, status: Optional[str] = None, department: Optional[str] = None) -> List[Dict]:
        """Get all workflows with optional filters."""
        results = self._workflows
        if status:
            results = [w for w in results if w["status"] == status]
        if department:
            results = [w for w in results if w["department"] == department]
        return results

    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """Get a single workflow by ID."""
        for w in self._workflows:
            if w["workflow_id"] == workflow_id:
                return w
        return None

    def get_summary_stats(self) -> Dict:
        """Get aggregate workflow statistics."""
        total = len(self._workflows)
        stuck = len([w for w in self._workflows if w["status"] == "stuck"])
        delayed = len([w for w in self._workflows if w["status"] == "delayed"])
        critical = len([w for w in self._workflows if w["status"] == "critical"])
        completed = len([w for w in self._workflows if w["status"] == "completed"])
        on_track = len([w for w in self._workflows if w["status"] == "on_track"])

        avg_days = sum(w["days_elapsed"] for w in self._workflows) / max(total, 1)
        sla_breached = len([w for w in self._workflows if w["sla_remaining"] == 0])

        return {
            "total_workflows": total,
            "on_track": on_track,
            "delayed": delayed,
            "stuck": stuck,
            "critical": critical,
            "completed": completed,
            "avg_days_elapsed": round(avg_days, 1),
            "sla_breach_count": sla_breached,
            "sla_compliance_rate": round((1 - sla_breached / max(total, 1)) * 100, 1),
        }

    def get_department_stats(self) -> List[Dict]:
        """Get per-department statistics."""
        dept_map = {}
        for w in self._workflows:
            dept = w["department"]
            if dept not in dept_map:
                dept_map[dept] = {"name": dept, "total": 0, "stuck": 0, "delayed": 0, "avg_days": []}
            dept_map[dept]["total"] += 1
            dept_map[dept]["avg_days"].append(w["days_elapsed"])
            if w["status"] == "stuck":
                dept_map[dept]["stuck"] += 1
            if w["status"] == "delayed":
                dept_map[dept]["delayed"] += 1

        result = []
        for dept, data in dept_map.items():
            avg = sum(data["avg_days"]) / max(len(data["avg_days"]), 1)
            bottleneck_score = round((data["stuck"] + data["delayed"]) / max(data["total"], 1) * 100, 1)
            result.append({
                "department": dept,
                "total_files": data["total"],
                "stuck_files": data["stuck"],
                "delayed_files": data["delayed"],
                "avg_processing_days": round(avg, 1),
                "bottleneck_score": bottleneck_score,
            })

        return sorted(result, key=lambda x: x["bottleneck_score"], reverse=True)


# Singleton instance
graph_engine = WorkflowGraphEngine()
