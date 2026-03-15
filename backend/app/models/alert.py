"""Alert and notification data models."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(str, Enum):
    SLA_BREACH_PREDICTED = "sla_breach_predicted"
    BOTTLENECK_DETECTED = "bottleneck_detected"
    FILE_STUCK = "file_stuck"
    ANOMALY_DETECTED = "anomaly_detected"
    HANDOFF_DELAY = "handoff_delay"


class Alert(BaseModel):
    alert_id: str
    workflow_id: str
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    description: str
    department: str
    officer_id: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    acknowledged: bool = False
    resolved: bool = False
    ai_recommendation: Optional[str] = None
    predicted_breach_date: Optional[datetime] = None
    confidence: float = 0.0  # 0-1 confidence score


class BottleneckReport(BaseModel):
    department: str
    stage: str
    avg_delay_days: float
    files_affected: int
    root_cause: str
    ai_recommendation: str
    potential_savings_days: float
    confidence: float
