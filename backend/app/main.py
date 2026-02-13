"""
FastAPI Application - Cloud Security Threat Predictor
Main application file with all REST API endpoints.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional

from .database import get_db, init_db
from .models import CloudLog
from .schemas import (
    LogResponse, AlertResponse, DashboardStats, 
    RiskTrendPoint, MessageResponse
)
from .simulator import (
    generate_normal_logs, 
    generate_anomalous_logs,
    generate_attack_simulation_logs
)
from .ml_model import CloudSecurityMLModel
from .risk_engine import RiskScoringEngine
from .explainer import AlertExplainer

# Initialize FastAPI app
app = FastAPI(
    title="Cloud Security Threat Predictor",
    description="AI-driven cloud security monitoring system with anomaly detection",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML model
ml_model = CloudSecurityMLModel()


@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    init_db()
    print("✅ Database initialized")
    
    # Load model if exists
    if ml_model.model_exists():
        ml_model.load_model()
        print("✅ ML model loaded from disk")


@app.get("/")
async def root():
    """Root endpoint - API status."""
    return {
        "message": "Cloud Security Threat Predictor API",
        "status": "active",
        "endpoints": {
            "generate_logs": "POST /generate-logs",
            "train_model": "POST /train-model",
            "analyze_logs": "POST /analyze-logs",
            "get_alerts": "GET /alerts",
            "dashboard_stats": "GET /dashboard-stats",
            "risk_trend": "GET /risk-trend",
            "simulate_attack": "POST /simulate-attack"
        }
    }


@app.post("/generate-logs", response_model=MessageResponse)
async def generate_logs(db: Session = Depends(get_db)):
    """
    Generate and store synthetic cloud logs.
    Creates 10,000 normal logs and 500 anomalous logs.
    """
    try:
        # Check if logs already exist
        existing_count = db.query(CloudLog).count()
        if existing_count > 0:
            return MessageResponse(
                message=f"Logs already exist ({existing_count} logs). Delete existing logs first if you want to regenerate.",
                details={"existing_logs": existing_count}
            )
        
        # Generate logs
        normal_logs = generate_normal_logs(10000)
        anomalous_logs = generate_anomalous_logs(500)
        
        all_logs = normal_logs + anomalous_logs
        
        # Store in database
        for log_data in all_logs:
            log = CloudLog(**log_data)
            db.add(log)
        
        db.commit()
        
        return MessageResponse(
            message="Successfully generated and stored logs",
            details={
                "normal_logs": len(normal_logs),
                "anomalous_logs": len(anomalous_logs),
                "total_logs": len(all_logs)
            }
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to generate logs: {str(e)}")


@app.post("/train-model", response_model=MessageResponse)
async def train_model(db: Session = Depends(get_db)):
    """
    Train the Isolation Forest model on normal logs only.
    The model learns patterns of normal behavior to detect anomalies.
    """
    try:
        # Get all normal logs (is_anomaly = False)
        normal_logs = db.query(CloudLog).filter(CloudLog.is_anomaly == False).all()
        
        if len(normal_logs) == 0:
            raise HTTPException(
                status_code=400,
                detail="No normal logs found. Generate logs first using /generate-logs"
            )
        
        # Convert to dictionaries
        log_dicts = [
            {
                'user_id': log.user_id,
                'login_location': log.login_location,
                'login_time': log.login_time,
                'failed_login_attempts': log.failed_login_attempts,
                'resource_access_level': log.resource_access_level,
                'vm_creation_count': log.vm_creation_count,
                'privilege_change': log.privilege_change
            }
            for log in normal_logs
        ]
        
        # Train model
        training_stats = ml_model.train(log_dicts)
        
        return MessageResponse(
            message="Model trained successfully",
            details=training_stats
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to train model: {str(e)}")


@app.post("/analyze-logs", response_model=MessageResponse)
async def analyze_logs(db: Session = Depends(get_db)):
    """
    Run anomaly detection and risk scoring on all logs.
    Updates logs with anomaly scores, risk scores, and risk levels.
    """
    try:
        # Check if model is trained
        if ml_model.model is None:
            if ml_model.model_exists():
                ml_model.load_model()
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Model not trained. Train the model first using /train-model"
                )
        
        # Get all logs
        all_logs = db.query(CloudLog).all()
        
        if len(all_logs) == 0:
            raise HTTPException(
                status_code=400,
                detail="No logs found. Generate logs first using /generate-logs"
            )
        
        # Convert to dictionaries for ML model
        log_dicts = [
            {
                'user_id': log.user_id,
                'login_location': log.login_location,
                'login_time': log.login_time,
                'failed_login_attempts': log.failed_login_attempts,
                'resource_access_level': log.resource_access_level,
                'vm_creation_count': log.vm_creation_count,
                'privilege_change': log.privilege_change
            }
            for log in all_logs
        ]
        
        # Predict anomaly scores
        predictions = ml_model.predict(log_dicts)
        
        # Update logs with scores
        alerts_created = 0
        for log, (anomaly_score, is_anomaly_pred) in zip(all_logs, predictions):
            # Calculate risk score
            risk_score, risk_level = RiskScoringEngine.calculate_and_classify(
                {
                    'failed_login_attempts': log.failed_login_attempts,
                    'privilege_change': log.privilege_change,
                    'vm_creation_count': log.vm_creation_count
                },
                anomaly_score
            )
            
            # Update log
            log.anomaly_score = anomaly_score
            log.risk_score = risk_score
            log.risk_level = risk_level
            
            if risk_level in ["Medium", "High"]:
                alerts_created += 1
        
        db.commit()
        
        return MessageResponse(
            message="Analysis completed successfully",
            details={
                "logs_analyzed": len(all_logs),
                "alerts_created": alerts_created
            }
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to analyze logs: {str(e)}")


@app.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(
    risk_level: Optional[str] = Query(None, description="Filter by risk level: Low, Medium, High"),
    limit: int = Query(100, description="Maximum number of alerts to return"),
    db: Session = Depends(get_db)
):
    """
    Get security alerts with explanations.
    Can filter by risk level and limit results.
    """
    try:
        # Build query
        query = db.query(CloudLog).filter(CloudLog.risk_score.isnot(None))
        
        # Filter by risk level if specified
        if risk_level:
            risk_level_capitalized = risk_level.capitalize()
            if risk_level_capitalized not in ["Low", "Medium", "High"]:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid risk level. Must be: Low, Medium, or High"
                )
            query = query.filter(CloudLog.risk_level == risk_level_capitalized)
        
        # Order by risk score (highest first) and apply limit
        alerts = query.order_by(CloudLog.risk_score.desc(), CloudLog.timestamp.desc()).limit(limit).all()
        
        # Generate explanations for each alert
        alert_responses = []
        for alert in alerts:
            # Convert to dict for explainer
            log_dict = {
                'user_id': alert.user_id,
                'login_location': alert.login_location,
                'login_time': alert.login_time,
                'failed_login_attempts': alert.failed_login_attempts,
                'resource_access_level': alert.resource_access_level,
                'vm_creation_count': alert.vm_creation_count,
                'privilege_change': alert.privilege_change,
                'anomaly_score': alert.anomaly_score,
                'risk_score': alert.risk_score,
                'risk_level': alert.risk_level
            }
            
            # Get feature importance if model is available
            top_features = None
            if ml_model.model is not None:
                try:
                    top_features = ml_model.get_feature_importance(log_dict)
                except:
                    pass  # If feature importance fails, continue without it
            
            # Generate explanation
            explanation = AlertExplainer.generate_explanation(log_dict, top_features)
            
            # Create response
            alert_response = AlertResponse(
                id=alert.id,
                user_id=alert.user_id,
                login_location=alert.login_location,
                login_time=alert.login_time,
                failed_login_attempts=alert.failed_login_attempts,
                resource_access_level=alert.resource_access_level,
                vm_creation_count=alert.vm_creation_count,
                privilege_change=alert.privilege_change,
                timestamp=alert.timestamp,
                risk_score=alert.risk_score,
                risk_level=alert.risk_level,
                explanation=explanation
            )
            alert_responses.append(alert_response)
        
        return alert_responses
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alerts: {str(e)}")


@app.get("/dashboard-stats", response_model=DashboardStats)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get dashboard statistics.
    Returns total logs, total alerts, and risk distribution.
    """
    try:
        # Total logs
        total_logs = db.query(CloudLog).count()
        
        # Total alerts (Medium + High risk)
        total_alerts = db.query(CloudLog).filter(
            CloudLog.risk_level.in_(["Medium", "High"])
        ).count()
        
        # Risk distribution
        low_risk = db.query(CloudLog).filter(CloudLog.risk_level == "Low").count()
        medium_risk = db.query(CloudLog).filter(CloudLog.risk_level == "Medium").count()
        high_risk = db.query(CloudLog).filter(CloudLog.risk_level == "High").count()
        
        return DashboardStats(
            total_logs=total_logs,
            total_alerts=total_alerts,
            low_risk=low_risk,
            medium_risk=medium_risk,
            high_risk=high_risk
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard stats: {str(e)}")


@app.get("/risk-trend", response_model=List[RiskTrendPoint])
async def get_risk_trend(
    hours: int = Query(24, description="Number of hours to look back"),
    db: Session = Depends(get_db)
):
    """
    Get risk trend over time.
    Returns average risk score and alert count for each hour.
    """
    try:
        # Calculate cutoff time
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        # Get logs within timeframe
        logs = db.query(CloudLog).filter(
            CloudLog.timestamp >= cutoff_time,
            CloudLog.risk_score.isnot(None)
        ).order_by(CloudLog.timestamp).all()
        
        # Group by hour
        hourly_data = {}
        for log in logs:
            hour_key = log.timestamp.strftime("%Y-%m-%d %H:00")
            
            if hour_key not in hourly_data:
                hourly_data[hour_key] = {
                    'scores': [],
                    'alerts': 0
                }
            
            hourly_data[hour_key]['scores'].append(log.risk_score)
            if log.risk_level in ["Medium", "High"]:
                hourly_data[hour_key]['alerts'] += 1
        
        # Calculate averages
        trend_points = []
        for hour_key in sorted(hourly_data.keys()):
            data = hourly_data[hour_key]
            avg_risk = sum(data['scores']) / len(data['scores']) if data['scores'] else 0
            
            trend_points.append(RiskTrendPoint(
                timestamp=hour_key,
                average_risk=round(avg_risk, 2),
                alert_count=data['alerts']
            ))
        
        # If no data, return empty trend
        if not trend_points:
            # Generate placeholder points
            for i in range(min(hours, 24)):
                hour_key = (datetime.utcnow() - timedelta(hours=hours-i)).strftime("%Y-%m-%d %H:00")
                trend_points.append(RiskTrendPoint(
                    timestamp=hour_key,
                    average_risk=0.0,
                    alert_count=0
                ))
        
        return trend_points
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch risk trend: {str(e)}")


@app.post("/simulate-attack", response_model=MessageResponse)
async def simulate_attack(db: Session = Depends(get_db)):
    """
    Simulate a security attack by injecting high-risk anomalous logs.
    Demonstrates the system's ability to detect and respond to threats.
    """
    try:
        # Check if model is trained
        if ml_model.model is None:
            if ml_model.model_exists():
                ml_model.load_model()
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Model not trained. Train the model first using /train-model"
                )
        
        # Generate attack logs
        attack_logs = generate_attack_simulation_logs(100)
        
        # Store logs
        new_log_ids = []
        for log_data in attack_logs:
            log = CloudLog(**log_data)
            db.add(log)
            db.flush()
            new_log_ids.append(log.id)
        
        db.commit()
        
        # Analyze the new attack logs
        new_logs = db.query(CloudLog).filter(CloudLog.id.in_(new_log_ids)).all()
        
        log_dicts = [
            {
                'user_id': log.user_id,
                'login_location': log.login_location,
                'login_time': log.login_time,
                'failed_login_attempts': log.failed_login_attempts,
                'resource_access_level': log.resource_access_level,
                'vm_creation_count': log.vm_creation_count,
                'privilege_change': log.privilege_change
            }
            for log in new_logs
        ]
        
        # Predict and score
        predictions = ml_model.predict(log_dicts)
        
        high_risk_count = 0
        for log, (anomaly_score, _) in zip(new_logs, predictions):
            risk_score, risk_level = RiskScoringEngine.calculate_and_classify(
                {
                    'failed_login_attempts': log.failed_login_attempts,
                    'privilege_change': log.privilege_change,
                    'vm_creation_count': log.vm_creation_count
                },
                anomaly_score
            )
            
            log.anomaly_score = anomaly_score
            log.risk_score = risk_score
            log.risk_level = risk_level
            
            if risk_level == "High":
                high_risk_count += 1
        
        db.commit()
        
        return MessageResponse(
            message="Attack simulation completed",
            details={
                "attack_logs_created": len(attack_logs),
                "high_risk_alerts": high_risk_count
            }
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to simulate attack: {str(e)}")


@app.delete("/reset-database")
async def reset_database(db: Session = Depends(get_db)):
    """
    Delete all logs from the database.
    Useful for testing and demo purposes.
    """
    try:
        deleted_count = db.query(CloudLog).delete()
        db.commit()
        
        return MessageResponse(
            message="Database reset successfully",
            details={"deleted_logs": deleted_count}
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to reset database: {str(e)}")
