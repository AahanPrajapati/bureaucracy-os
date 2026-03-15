"""Department and officer data models."""

from pydantic import BaseModel
from typing import Optional, List


class Officer(BaseModel):
    officer_id: str
    name: str
    designation: str
    department_id: str
    active_files: int = 0
    avg_processing_days: float = 0.0


class Department(BaseModel):
    department_id: str
    name: str
    state: str
    district: Optional[str] = None
    officers: List[Officer] = []
    active_workflows: int = 0
    avg_sla_compliance: float = 0.0
    bottleneck_score: float = 0.0  # 0-100, higher = more bottlenecked
