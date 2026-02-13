"""
Machine Learning Model Module
Implements Isolation Forest for anomaly detection in cloud logs.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os
from typing import List, Dict, Tuple


class CloudSecurityMLModel:
    """
    ML model for detecting anomalies in cloud activity logs.
    Uses Isolation Forest algorithm trained only on normal behavior.
    """
    
    def __init__(self, model_path: str = "isolation_forest_model.joblib"):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.location_encoder = LabelEncoder()
        self.resource_encoder = LabelEncoder()
        self.feature_names = []
        
    def preprocess_data(self, logs: List[Dict], fit: bool = False) -> pd.DataFrame:
        """
        Preprocess raw log data into features for ML model.
        
        Feature engineering:
        - Encode categorical variables (location, resource_access_level)
        - Normalize numerical values
        - Extract behavioral features (login_frequency, unusual_location_flag, etc.)
        
        Args:
            logs: List of log dictionaries
            fit: If True, fit encoders and scaler (for training data)
            
        Returns:
            DataFrame with engineered features
        """
        df = pd.DataFrame(logs)
        
        # Feature engineering
        # 1. Login frequency per user (count of logs per user)
        user_counts = df['user_id'].value_counts().to_dict()
        df['login_frequency'] = df['user_id'].map(user_counts)
        
        # 2. Unusual location flag
        unusual_locations = ["Unknown", "Tor-Exit-Node", "Darknet", "Suspicious-IP", "Blacklisted-Region"]
        df['unusual_location_flag'] = df['login_location'].isin(unusual_locations).astype(int)
        
        # 3. Privilege escalation flag
        df['privilege_escalation_flag'] = df['privilege_change'].astype(int)
        
        # 4. Access spike score (combination of failed logins and VM creation)
        df['access_spike_score'] = (
            df['failed_login_attempts'] * 0.3 + 
            df['vm_creation_count'] * 0.7
        )
        
        # 5. Hour of login (extract from login_time)
        df['login_hour'] = pd.to_datetime(df['login_time'], format='%H:%M').dt.hour
        
        # 6. Resource access level encoding
        resource_mapping = {'low': 0, 'medium': 1, 'high': 2}
        df['resource_access_encoded'] = df['resource_access_level'].map(resource_mapping)
        
        # Encode categorical location
        if fit:
            df['location_encoded'] = self.location_encoder.fit_transform(df['login_location'])
        else:
            # Handle unseen categories
            df['location_encoded'] = df['login_location'].apply(
                lambda x: self.location_encoder.transform([x])[0] 
                if x in self.location_encoder.classes_ 
                else -1
            )
        
        # Select features for model
        feature_cols = [
            'failed_login_attempts',
            'vm_creation_count',
            'login_frequency',
            'unusual_location_flag',
            'privilege_escalation_flag',
            'access_spike_score',
            'login_hour',
            'resource_access_encoded',
            'location_encoded'
        ]
        
        X = df[feature_cols]
        self.feature_names = feature_cols
        
        # Normalize features
        if fit:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        return pd.DataFrame(X_scaled, columns=feature_cols)
    
    def train(self, normal_logs: List[Dict]) -> Dict:
        """
        Train Isolation Forest on normal logs only.
        
        The model learns the pattern of normal behavior and can then
        identify deviations (anomalies) in new data.
        
        Args:
            normal_logs: List of normal (non-anomalous) log dictionaries
            
        Returns:
            Dictionary with training statistics
        """
        # Preprocess training data
        X_train = self.preprocess_data(normal_logs, fit=True)
        
        # Initialize and train Isolation Forest
        # contamination='auto' assumes normal data may have slight noise
        # n_estimators=100 creates 100 decision trees
        # random_state for reproducibility
        self.model = IsolationForest(
            contamination=0.05,  # Expect ~5% contamination in "normal" data
            n_estimators=100,
            max_samples='auto',
            random_state=42,
            n_jobs=-1  # Use all CPU cores
        )
        
        self.model.fit(X_train)
        
        # Save model and preprocessing objects
        self.save_model()
        
        return {
            "training_samples": len(normal_logs),
            "features": self.feature_names,
            "model_type": "IsolationForest",
            "contamination": 0.05
        }
    
    def predict(self, logs: List[Dict]) -> List[Tuple[float, bool]]:
        """
        Predict anomaly scores for new logs.
        
        Returns anomaly score between 0 and 1:
        - 0.0 = definitely normal
        - 1.0 = definitely anomalous
        
        Args:
            logs: List of log dictionaries to analyze
            
        Returns:
            List of tuples (anomaly_score, is_anomaly)
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first or load_model().")
        
        # Preprocess data
        X = self.preprocess_data(logs, fit=False)
        
        # Get anomaly scores
        # Isolation Forest returns:
        # -1 for anomalies, 1 for normal points
        # decision_function returns raw anomaly scores (higher = more anomalous)
        raw_scores = self.model.decision_function(X)
        predictions = self.model.predict(X)
        
        # Convert to 0-1 range (normalize scores)
        # Use min-max scaling on raw scores
        min_score = raw_scores.min()
        max_score = raw_scores.max()
        
        if max_score - min_score > 0:
            normalized_scores = (raw_scores - min_score) / (max_score - min_score)
            # Invert so higher score = more anomalous
            anomaly_scores = 1 - normalized_scores
        else:
            anomaly_scores = np.zeros(len(raw_scores))
        
        # Combine scores with binary predictions
        results = [
            (float(score), bool(pred == -1))
            for score, pred in zip(anomaly_scores, predictions)
        ]
        
        return results
    
    def get_feature_importance(self, log: Dict) -> List[Tuple[str, float]]:
        """
        Get feature importance for a specific log entry.
        Returns top contributing features for explainability.
        
        Args:
            log: Single log dictionary
            
        Returns:
            List of (feature_name, importance_score) tuples, sorted by importance
        """
        # Preprocess single log
        X = self.preprocess_data([log], fit=False)
        
        # Get feature values
        feature_values = X.iloc[0].to_dict()
        
        # Simple importance: absolute value of each feature (after normalization)
        # Higher absolute values contribute more to anomaly detection
        importances = [
            (name, abs(value))
            for name, value in feature_values.items()
        ]
        
        # Sort by importance
        importances.sort(key=lambda x: x[1], reverse=True)
        
        return importances[:5]  # Return top 5 features
    
    def save_model(self):
        """Save trained model and preprocessing objects to disk."""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'location_encoder': self.location_encoder,
            'resource_encoder': self.resource_encoder,
            'feature_names': self.feature_names
        }
        joblib.dump(model_data, self.model_path)
    
    def load_model(self):
        """Load trained model and preprocessing objects from disk."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        
        model_data = joblib.load(self.model_path)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.location_encoder = model_data['location_encoder']
        self.resource_encoder = model_data['resource_encoder']
        self.feature_names = model_data['feature_names']
    
    def model_exists(self) -> bool:
        """Check if trained model file exists."""
        return os.path.exists(self.model_path)
