"""
Cloud Log Simulator Module
Generates synthetic cloud activity logs with normal and anomalous patterns.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict


# Define realistic data distributions
LOCATIONS_NORMAL = ["US-East", "US-West", "EU-West", "EU-Central", "Asia-Pacific"]
LOCATIONS_UNUSUAL = ["Unknown", "Tor-Exit-Node", "Darknet", "Suspicious-IP", "Blacklisted-Region"]
RESOURCE_LEVELS = ["low", "medium", "high"]
USER_IDS = [f"user_{i:04d}" for i in range(1, 501)]  # 500 users


def generate_normal_logs(count: int = 10000) -> List[Dict]:
    """
    Generate normal (non-anomalous) cloud activity logs.
    
    Normal behavior characteristics:
    - Standard login locations
    - Low failed login attempts (0-2)
    - No privilege changes
    - Low VM creation (0-2)
    - Standard resource access
    
    Args:
        count: Number of normal logs to generate
        
    Returns:
        List of dictionaries containing log data
    """
    logs = []
    base_time = datetime.utcnow() - timedelta(days=7)  # Start from 7 days ago
    
    for i in range(count):
        # Generate realistic timestamp
        timestamp = base_time + timedelta(
            seconds=random.randint(0, 7 * 24 * 3600)  # Random time within 7 days
        )
        
        log = {
            "user_id": random.choice(USER_IDS),
            "login_location": random.choice(LOCATIONS_NORMAL),
            "login_time": timestamp.strftime("%H:%M"),
            "failed_login_attempts": random.randint(0, 2),  # Normal: 0-2 failures
            "resource_access_level": random.choices(
                RESOURCE_LEVELS,
                weights=[0.6, 0.3, 0.1]  # Mostly low/medium access
            )[0],
            "vm_creation_count": random.randint(0, 2),  # Normal: 0-2 VMs
            "privilege_change": False,  # Normal: no privilege escalation
            "timestamp": timestamp,
            "is_anomaly": False
        }
        logs.append(log)
    
    return logs


def generate_anomalous_logs(count: int = 500) -> List[Dict]:
    """
    Generate anomalous (suspicious) cloud activity logs.
    
    Anomalous behavior characteristics:
    - Unusual/suspicious locations
    - High failed login attempts (5-15)
    - Privilege changes (escalation)
    - Excessive VM creation (5-20)
    - High resource access patterns
    
    Args:
        count: Number of anomalous logs to generate
        
    Returns:
        List of dictionaries containing anomalous log data
    """
    logs = []
    base_time = datetime.utcnow() - timedelta(days=7)
    
    for i in range(count):
        timestamp = base_time + timedelta(
            seconds=random.randint(0, 7 * 24 * 3600)
        )
        
        # Create different types of anomalies
        anomaly_type = random.choice([
            "unusual_location",
            "failed_logins",
            "privilege_escalation",
            "vm_spike",
            "combined"
        ])
        
        if anomaly_type == "unusual_location":
            log = {
                "user_id": random.choice(USER_IDS),
                "login_location": random.choice(LOCATIONS_UNUSUAL),
                "login_time": timestamp.strftime("%H:%M"),
                "failed_login_attempts": random.randint(1, 5),
                "resource_access_level": random.choice(RESOURCE_LEVELS),
                "vm_creation_count": random.randint(0, 3),
                "privilege_change": random.choice([True, False]),
                "timestamp": timestamp,
                "is_anomaly": True
            }
        elif anomaly_type == "failed_logins":
            log = {
                "user_id": random.choice(USER_IDS),
                "login_location": random.choice(LOCATIONS_NORMAL),
                "login_time": timestamp.strftime("%H:%M"),
                "failed_login_attempts": random.randint(5, 15),  # High failures
                "resource_access_level": random.choice(RESOURCE_LEVELS),
                "vm_creation_count": random.randint(0, 3),
                "privilege_change": False,
                "timestamp": timestamp,
                "is_anomaly": True
            }
        elif anomaly_type == "privilege_escalation":
            log = {
                "user_id": random.choice(USER_IDS),
                "login_location": random.choice(LOCATIONS_NORMAL),
                "login_time": timestamp.strftime("%H:%M"),
                "failed_login_attempts": random.randint(0, 3),
                "resource_access_level": "high",  # Elevated access
                "vm_creation_count": random.randint(0, 5),
                "privilege_change": True,  # Privilege escalation!
                "timestamp": timestamp,
                "is_anomaly": True
            }
        elif anomaly_type == "vm_spike":
            log = {
                "user_id": random.choice(USER_IDS),
                "login_location": random.choice(LOCATIONS_NORMAL),
                "login_time": timestamp.strftime("%H:%M"),
                "failed_login_attempts": random.randint(0, 3),
                "resource_access_level": random.choice(RESOURCE_LEVELS),
                "vm_creation_count": random.randint(5, 20),  # Excessive VM creation
                "privilege_change": False,
                "timestamp": timestamp,
                "is_anomaly": True
            }
        else:  # combined - multiple suspicious factors
            log = {
                "user_id": random.choice(USER_IDS),
                "login_location": random.choice(LOCATIONS_UNUSUAL),
                "login_time": timestamp.strftime("%H:%M"),
                "failed_login_attempts": random.randint(5, 15),
                "resource_access_level": "high",
                "vm_creation_count": random.randint(5, 15),
                "privilege_change": True,
                "timestamp": timestamp,
                "is_anomaly": True
            }
        
        logs.append(log)
    
    return logs


def generate_attack_simulation_logs(count: int = 100) -> List[Dict]:
    """
    Generate high-risk attack simulation logs.
    Used for the "Simulate Attack" feature.
    
    Args:
        count: Number of attack logs to generate
        
    Returns:
        List of high-risk anomalous logs
    """
    logs = []
    current_time = datetime.utcnow()
    
    for i in range(count):
        # Generate recent timestamps (within last hour)
        timestamp = current_time - timedelta(minutes=random.randint(0, 60))
        
        log = {
            "user_id": random.choice(USER_IDS[:50]),  # Target specific users
            "login_location": random.choice(LOCATIONS_UNUSUAL),
            "login_time": timestamp.strftime("%H:%M"),
            "failed_login_attempts": random.randint(10, 20),  # Very high
            "resource_access_level": "high",
            "vm_creation_count": random.randint(10, 25),  # Very high
            "privilege_change": True,
            "timestamp": timestamp,
            "is_anomaly": True
        }
        logs.append(log)
    
    return logs
