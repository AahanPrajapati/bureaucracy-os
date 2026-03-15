"""Workflow and file tracking data models."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class WorkflowStatus(str, Enum):
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    STUCK = "stuck"
    COMPLETED = "completed"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WorkflowStage(BaseModel):
    stage_id: str
    name: str
    department: str
    officer: Optional[str] = None
    entered_at: datetime
    completed_at: Optional[datetime] = None
    expected_duration_days: int
    actual_duration_days: Optional[int] = None
    status: WorkflowStatus = WorkflowStatus.IN_REVIEW


class WorkflowEvent(BaseModel):
    event_id: str = Field(..., description="Unique event identifier")
    workflow_id: str
    event_type: str  # "file_moved", "approval_granted", "review_started", etc.
    from_department: Optional[str] = None
    to_department: Optional[str] = None
    officer_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = {}


class Workflow(BaseModel):
    workflow_id: str
    title: str
    description: Optional[str] = None
    file_number: str
    department: str
    initiated_by: str
    priority: Priority = Priority.MEDIUM
    status: WorkflowStatus = WorkflowStatus.SUBMITTED
    stages: List[WorkflowStage] = []
    current_stage: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    expected_completion: Optional[datetime] = None
    sla_days: int = 30
    tags: List[str] = []


class WorkflowSummary(BaseModel):
    total_workflows: int
    active: int
    stuck: int
    completed: int
    avg_completion_days: float
    sla_breach_rate: float
