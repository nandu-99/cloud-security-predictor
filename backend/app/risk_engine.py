"""
Risk Scoring Engine
Calculates dynamic risk scores based on anomaly detection and log features.
"""

from typing import Dict, Tuple


class RiskScoringEngine:
    """
    Calculates risk scores for cloud activity logs.
    Combines ML anomaly scores with rule-based risk factors.
    """
    
    # Risk score weights
    ANOMALY_WEIGHT = 50
    FAILED_LOGIN_WEIGHT = 5
    PRIVILEGE_CHANGE_WEIGHT = 20
    VM_CREATION_WEIGHT = 5
    
    # Risk level thresholds
    LOW_THRESHOLD = 30
    MEDIUM_THRESHOLD = 70
    
    @staticmethod
    def calculate_risk_score(
        anomaly_score: float,
        failed_login_attempts: int,
        privilege_change: bool,
        vm_creation_count: int
    ) -> float:
        """
        Calculate weighted risk score (0-100).
        
        Formula:
        Risk Score = (anomaly_score * 50) +
                     (failed_login_attempts * 5) +
                     (privilege_change * 20) +
                     (vm_creation_count * 5)
        
        Args:
            anomaly_score: ML model anomaly score (0-1)
            failed_login_attempts: Number of failed login attempts
            privilege_change: Boolean indicating privilege escalation
            vm_creation_count: Number of VMs created
            
        Returns:
            Risk score between 0 and 100
        """
        score = (
            anomaly_score * RiskScoringEngine.ANOMALY_WEIGHT +
            failed_login_attempts * RiskScoringEngine.FAILED_LOGIN_WEIGHT +
            (1 if privilege_change else 0) * RiskScoringEngine.PRIVILEGE_CHANGE_WEIGHT +
            vm_creation_count * RiskScoringEngine.VM_CREATION_WEIGHT
        )
        
        # Cap at 100
        return min(score, 100.0)
    
    @staticmethod
    def classify_risk_level(risk_score: float) -> str:
        """
        Classify risk score into Low/Medium/High categories.
        
        Classification:
        - 0-30: Low
        - 31-70: Medium
        - 71-100: High
        
        Args:
            risk_score: Calculated risk score (0-100)
            
        Returns:
            Risk level string: "Low", "Medium", or "High"
        """
        if risk_score <= RiskScoringEngine.LOW_THRESHOLD:
            return "Low"
        elif risk_score <= RiskScoringEngine.MEDIUM_THRESHOLD:
            return "Medium"
        else:
            return "High"
    
    @staticmethod
    def calculate_and_classify(log_data: Dict, anomaly_score: float) -> Tuple[float, str]:
        """
        Calculate risk score and classify in one step.
        
        Args:
            log_data: Dictionary containing log attributes
            anomaly_score: ML model anomaly score
            
        Returns:
            Tuple of (risk_score, risk_level)
        """
        risk_score = RiskScoringEngine.calculate_risk_score(
            anomaly_score=anomaly_score,
            failed_login_attempts=log_data.get('failed_login_attempts', 0),
            privilege_change=log_data.get('privilege_change', False),
            vm_creation_count=log_data.get('vm_creation_count', 0)
        )
        
        risk_level = RiskScoringEngine.classify_risk_level(risk_score)
        
        return risk_score, risk_level
