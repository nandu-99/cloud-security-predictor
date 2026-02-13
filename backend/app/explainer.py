"""
Explainable AI Layer
Generates human-readable explanations for security alerts.
"""

from typing import List, Dict


class AlertExplainer:
    """
    Generates explainable AI insights for security alerts.
    Provides human-readable reasons for why an alert was flagged.
    """
    
    @staticmethod
    def generate_explanation(log_data: Dict, top_features: List = None) -> List[str]:
        """
        Generate explanation for a security alert.
        
        Analyzes log attributes and ML feature importance to create
        human-readable explanations.
        
        Args:
            log_data: Dictionary containing log attributes
            top_features: Optional list of (feature_name, importance) tuples from ML model
            
        Returns:
            List of explanation strings describing risk factors
        """
        explanations = []
        
        # Check for unusual location
        unusual_locations = ["Unknown", "Tor-Exit-Node", "Darknet", "Suspicious-IP", "Blacklisted-Region"]
        if log_data.get('login_location') in unusual_locations:
            explanations.append(
                f"⚠️ Unusual login location detected: {log_data['login_location']}"
            )
        
        # Check for failed login attempts
        failed_attempts = log_data.get('failed_login_attempts', 0)
        if failed_attempts >= 5:
            explanations.append(
                f"🔒 Multiple failed login attempts: {failed_attempts} failures"
            )
        elif failed_attempts >= 3:
            explanations.append(
                f"⚠️ Elevated failed login attempts: {failed_attempts} failures"
            )
        
        # Check for privilege escalation
        if log_data.get('privilege_change'):
            explanations.append(
                "🔐 Privilege escalation detected - unauthorized elevation of permissions"
            )
        
        # Check for VM creation spike
        vm_count = log_data.get('vm_creation_count', 0)
        if vm_count >= 10:
            explanations.append(
                f"💻 Suspicious VM creation activity: {vm_count} VMs created"
            )
        elif vm_count >= 5:
            explanations.append(
                f"⚠️ Elevated VM creation: {vm_count} VMs created"
            )
        
        # Check for high resource access
        if log_data.get('resource_access_level') == 'high':
            explanations.append(
                "🔑 High-level resource access requested"
            )
        
        # Check for unusual time
        login_time = log_data.get('login_time', '')
        if login_time:
            hour = int(login_time.split(':')[0])
            if hour < 6 or hour > 22:  # Outside normal business hours
                explanations.append(
                    f"🕐 Login during unusual hours: {login_time}"
                )
        
        # If ML model provided feature importance, add that context
        if top_features:
            ml_factors = []
            for feature_name, importance in top_features[:3]:
                if importance > 0.5:  # Only mention significant features
                    readable_name = feature_name.replace('_', ' ').title()
                    ml_factors.append(readable_name)
            
            if ml_factors:
                explanations.append(
                    f"🤖 ML model identified key risk factors: {', '.join(ml_factors)}"
                )
        
        # If no specific factors found, provide general explanation
        if not explanations:
            anomaly_score = log_data.get('anomaly_score', 0)
            if anomaly_score and anomaly_score > 0.6:
                explanations.append(
                    "🔍 Behavioral pattern deviates significantly from normal activity"
                )
            else:
                explanations.append(
                    "ℹ️ Multiple minor risk indicators combined"
                )
        
        return explanations
    
    @staticmethod
    def get_risk_summary(risk_level: str, risk_score: float) -> str:
        """
        Generate a summary message for the risk level.
        
        Args:
            risk_level: Risk classification (Low/Medium/High)
            risk_score: Numerical risk score (0-100)
            
        Returns:
            Summary string
        """
        summaries = {
            "Low": f"✅ Low Risk (Score: {risk_score:.1f}/100) - Activity within normal parameters",
            "Medium": f"⚠️ Medium Risk (Score: {risk_score:.1f}/100) - Suspicious behavior detected, monitor closely",
            "High": f"🚨 High Risk (Score: {risk_score:.1f}/100) - Critical threat detected, immediate action required"
        }
        
        return summaries.get(risk_level, f"Risk Score: {risk_score:.1f}/100")
    
    @staticmethod
    def format_alert_details(log_data: Dict) -> Dict:
        """
        Format log data into structured alert details.
        
        Args:
            log_data: Raw log dictionary
            
        Returns:
            Formatted dictionary with readable keys and values
        """
        return {
            "User ID": log_data.get('user_id', 'Unknown'),
            "Login Location": log_data.get('login_location', 'Unknown'),
            "Login Time": log_data.get('login_time', 'Unknown'),
            "Failed Attempts": log_data.get('failed_login_attempts', 0),
            "Resource Level": log_data.get('resource_access_level', 'Unknown'),
            "VMs Created": log_data.get('vm_creation_count', 0),
            "Privilege Change": "Yes" if log_data.get('privilege_change') else "No",
            "Anomaly Score": f"{log_data.get('anomaly_score', 0):.2f}",
            "Risk Score": f"{log_data.get('risk_score', 0):.1f}/100",
            "Risk Level": log_data.get('risk_level', 'Unknown')
        }
