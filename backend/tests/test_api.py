"""Tests for Bureaucracy OS API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Bureaucracy OS"
    assert data["status"] == "operational"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_workflows():
    response = client.get("/api/v1/workflows/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "workflows" in data
    assert data["total"] > 0


def test_workflow_summary():
    response = client.get("/api/v1/workflows/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_workflows" in data
    assert "sla_compliance_rate" in data


def test_department_stats():
    response = client.get("/api/v1/workflows/departments")
    assert response.status_code == 200
    data = response.json()
    assert "departments" in data
    assert len(data["departments"]) > 0


def test_get_single_workflow():
    # First get list to find a valid ID
    response = client.get("/api/v1/workflows/")
    workflows = response.json()["workflows"]
    wf_id = workflows[0]["workflow_id"]

    response = client.get(f"/api/v1/workflows/{wf_id}")
    assert response.status_code == 200


def test_workflow_not_found():
    response = client.get("/api/v1/workflows/NONEXISTENT-999")
    assert response.status_code == 404


def test_ingest_event():
    event = {
        "event_id": "EVT-001",
        "workflow_id": "WF-2024-0001",
        "event_type": "file_moved",
        "from_department": "Finance",
        "to_department": "Legal",
    }
    response = client.post("/api/v1/workflows/ingest", json=event)
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"


def test_alerts():
    response = client.get("/api/v1/alerts/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "alerts" in data


def test_bottlenecks():
    response = client.get("/api/v1/analytics/bottlenecks")
    assert response.status_code == 200
    data = response.json()
    assert "bottlenecks" in data


def test_sla_predictions():
    response = client.get("/api/v1/analytics/predictions")
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data


def test_efficiency_metrics():
    response = client.get("/api/v1/analytics/efficiency")
    assert response.status_code == 200
    data = response.json()
    assert "total_active_files" in data
    assert "sla_compliance_trend" in data


def test_risk_distribution():
    response = client.get("/api/v1/analytics/risk-distribution")
    assert response.status_code == 200
    data = response.json()
    assert "distribution" in data


def test_minister_dashboard():
    response = client.get("/api/v1/dashboard/minister")
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "minister"
    assert "summary" in data
    assert "top_bottlenecks" in data


def test_officer_dashboard():
    response = client.get("/api/v1/dashboard/officer")
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "officer"


def test_citizen_portal():
    response = client.get("/api/v1/dashboard/citizen/WF-2024-0001")
    assert response.status_code == 200
    data = response.json()
    assert "stages" in data
