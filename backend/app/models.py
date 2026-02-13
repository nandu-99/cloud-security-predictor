"""
SQLAlchemy models for Cloud Security application.
Defines the CloudLog table structure for storing synthetic cloud activity logs.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Index
from datetime import datetime
from .database import Base


class CloudLog(Base):
    """
    Model representing a cloud activity log entry.
    Stores user activity, risk metrics, and anomaly detection results.
    """
    __tablename__ = "cloud_logs"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Log attributes (input features)
    user_id = Column(String(50), nullable=False, index=True)
    login_location = Column(String(100), nullable=False)
    login_time = Column(String(20), nullable=False)  # Time of day (e.g., "14:30")
    failed_login_attempts = Column(Integer, default=0)
    resource_access_level = Column(String(20), nullable=False)  # low/medium/high
    vm_creation_count = Column(Integer, default=0)
    privilege_change = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # ML-generated attributes
    is_anomaly = Column(Boolean, default=False)  # Ground truth label
    anomaly_score = Column(Float, nullable=True)  # Model prediction (0-1)
    
    # Risk scoring
    risk_score = Column(Float, nullable=True)  # Calculated risk (0-100)
    risk_level = Column(String(20), nullable=True, index=True)  # Low/Medium/High
    
    # Feature engineering (computed during preprocessing)
    login_frequency = Column(Integer, default=0)
    unusual_location_flag = Column(Boolean, default=False)
    privilege_escalation_flag = Column(Boolean, default=False)
    access_spike_score = Column(Float, default=0.0)

    def __repr__(self):
        return f"<CloudLog(id={self.id}, user={self.user_id}, risk={self.risk_level})>"


# Create indexes for common queries
Index('idx_risk_timestamp', CloudLog.risk_level, CloudLog.timestamp)
Index('idx_anomaly', CloudLog.is_anomaly)
