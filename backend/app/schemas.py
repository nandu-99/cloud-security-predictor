"""
Pydantic schemas for request/response validation.
Defines data structures for API endpoints.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class LogResponse(BaseModel):
    """Schema for individual log response"""
    id: int
    user_id: str
    login_location: str
    login_time: str
    failed_login_attempts: int
    resource_access_level: str
    vm_creation_count: int
    privilege_change: bool
    timestamp: datetime
    anomaly_score: Optional[float] = None
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    
    class Config:
        from_attributes = True


class AlertResponse(BaseModel):
    """Schema for alert with explanation"""
    id: int
    user_id: str
    login_location: str
    login_time: str
    failed_login_attempts: int
    resource_access_level: str
    vm_creation_count: int
    privilege_change: bool
    timestamp: datetime
    risk_score: float
    risk_level: str
    explanation: List[str]  # List of contributing factors
    
    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    """Schema for dashboard statistics"""
    total_logs: int
    total_alerts: int
    low_risk: int
    medium_risk: int
    high_risk: int


class RiskTrendPoint(BaseModel):
    """Schema for risk trend data point"""
    timestamp: str
    average_risk: float
    alert_count: int


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    details: Optional[dict] = None
