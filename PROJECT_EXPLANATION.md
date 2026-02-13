# Cloud Security Threat Predictor - Project Explanation

## 🛡️ Project Overview

The **Cloud Security Threat Predictor** is an AI-driven system designed to monitor, detect, and predict security threats in cloud environments. It simulates a real-world cloud infrastructure where users perform various actions (logging in, accessing resources, creating VMs, changing privileges).

The system uses **Machine Learning (Isolation Forest)** to learn "normal" user behavior and detect anomalies that could indicate security breaches, such as:
- **Insider Threats**: Legitimate users behaving suspiciously.
- **Account Compromise**: Unusual login locations or times.
- **Brute Force Attacks**: High number of failed login attempts.
- **Privilege Escalation**: Unauthorized changes in access rights.

---

## 🏗️ System Architecture

The project follows a modern **Client-Server Architecture**:

### 1. Frontend (User Interface)
- **Tech Stack**: React.js, Vite, Tailwind CSS.
- **Purpose**: Provides an interactive dashboard for security analysts to monitor the system status, view real-time alerts, and control the simulation.
- **Key Features**:
  - **Dashboard**: Displays high-level statistics (Total Logs, Alerts, Risk Distribution).
  - **Risk Trend Chart**: Visualizes risk scores over the last 24 hours.
  - **Alerts Table**: Lists detected threats with AI-generated explanations.
  - **Control Panel**: Buttons to trigger log generation, model training, and attack simulations.

### 2. Backend (API & Logic)
- **Tech Stack**: Python, FastAPI, SQLAlchemy, Scikit-learn.
- **Purpose**: Handles data processing, machine learning, and API requests.
- **Key Components**:
  - **API Layer (`main.py`)**: Exposes REST endpoints for the frontend.
  - **ML Engine (`ml_model.py`)**: Trains and runs the Isolation Forest model.
  - **Risk Engine (`risk_engine.py`)**: Calculates risk scores based on ML output and heuristic rules.
  - **Simulator (`simulator.py`)**: Generates synthetic log data to mimic cloud user activity.

### 3. Database (Storage)
- **Tech Stack**: SQLite (dev) / PostgreSQL (prod).
- **Purpose**: Stores all log data, user profiles, and alert history.
- **File**: `backend/cloud_security.db`.

---

## 🧠 Core Logic & Workflow

### Step 1: Data Simulation (`/generate-logs`)
The system generates synthetic logs representing user activities.
- **Normal Logs**: Regular users from known locations performing standard tasks.
- **Anomalous Logs**: Unusual behaviors like logging in from "Darknet" or "Tor-Exit-Node", high failed logins, etc.

### Step 2: Model Training (`/train-model`)
The **Isolation Forest** algorithm is trained **only on normal logs**.
- It learns the distribution of "normal" behavior.
- Features used: `login_frequency`, `unusual_location_flag`, `privilege_escalation_flag`, `access_spike_score`, `login_hour`, etc.

### Step 3: Anomaly Detection (`/analyze-logs`)
When new logs are analyzed:
1. The ML model assigns an **Anomaly Score** (0 to 1). Higher score = more anomalous.
2. The **Risk Engine** combines this with rule-based factors to calculate a **Risk Score** (0-100).

**Risk Formula**:
```python
Risk Score = (Anomaly Score * 50) +
             (Failed Login Attempts * 5) +
             (Privilege Change * 20) +
             (VM Creation Count * 5)
```

### Step 4: Risk Classification
Scores are classified into levels:
- **Low (0-30)**: Normal activity.
- **Medium (31-70)**: Suspicious, warrants investigation.
- **High (71-100)**: Critical threat, immediate action required.

### Step 5: Attack Simulation (`/simulate-attack`)
Injects high-risk patterns (e.g., massive data exfiltration, unauthorized admin access) to test the system's detection capabilities.

---

## 📂 Directory Structure Highlights

### Backend (`/backend`)
- **`app/main.py`**: Entry point, defines all API routes.
- **`app/ml_model.py`**: Contains the `CloudSecurityMLModel` class for training and prediction.
- **`app/risk_engine.py`**: Logic for converting anomaly scores into business risk scores.
- **`app/simulator.py`**: Scripts to generate realistic synthetic data.
- **`app/models.py`**: Database schema definitions (SQLAlchemy models).

### Frontend (`/frontend`)
- **`src/components/Dashboard.jsx`**: Main view combining all sub-components.
- **`src/components/RiskChart.jsx`**: Renders the risk trend graph using Recharts.
- **`src/components/AlertsTable.jsx`**: Displays list of alerts with filtering.
- **`src/services/api.js`**: Axios configuration for communicating with the backend.

---

## 🚀 Getting Started

1. **Start Backend**:
   ```bash
   cd backend
   ./start.sh
   ```
   Server runs at `http://localhost:8000`.

2. **Start Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   App runs at `http://localhost:5173`.
