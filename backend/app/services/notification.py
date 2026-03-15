"""
Notification Service — Layer 4 (The Voice)
Handles SMS, WhatsApp, and email alerts for critical workflow updates.
"""

from typing import List, Dict
from datetime import datetime


class NotificationService:
    """
    In production, integrates with:
    - Twilio / MSG91 for SMS
    - WhatsApp Business API
    - SMTP for email
    
    For prototype, we log notifications.
    """

    def __init__(self):
        self._notification_log: List[Dict] = []

    def send_sla_alert(self, workflow_id: str, officer_id: str, breach_in_days: int) -> Dict:
        notification = {
            "id": f"NOTIF-{len(self._notification_log) + 1:04d}",
            "type": "sla_alert",
            "workflow_id": workflow_id,
            "recipient": officer_id,
            "channel": "sms+email",
            "message": f"SLA Alert: File {workflow_id} is predicted to breach deadline in {breach_in_days} days. Immediate action required.",
            "sent_at": datetime.utcnow().isoformat(),
            "status": "sent",
        }
        self._notification_log.append(notification)
        return notification

    def send_bottleneck_alert(self, department: str, files_affected: int, recommendation: str) -> Dict:
        notification = {
            "id": f"NOTIF-{len(self._notification_log) + 1:04d}",
            "type": "bottleneck_alert",
            "department": department,
            "channel": "email+whatsapp",
            "message": f"Bottleneck detected in {department}: {files_affected} files affected. AI Recommendation: {recommendation}",
            "sent_at": datetime.utcnow().isoformat(),
            "status": "sent",
        }
        self._notification_log.append(notification)
        return notification

    def get_notification_log(self, limit: int = 50) -> List[Dict]:
        return self._notification_log[-limit:]


notification_service = NotificationService()
