# Cloud Security Threat Predictor

## 🛡️ Overview

The **Cloud Security Threat Predictor** is an AI-driven system designed to detect and predict security threats in cloud environments. It leverages machine learning to analyze user behavior, identify anomalies, and generate real-time alerts for potential security breaches.

The system consists of:
- **Frontend**: A modern, responsive React application for visualizing threat data, calculating risk scores, and managing alerts.
- **Backend**: A FastAPI-based server that handles log ingestion, ML model training, and threat analysis.
- **Database**: PostgreSQL for structured data and Elasticsearch for log storage.

## 🚀 Local Setup

Follow these instructions to set up and run the project locally.

### Prerequisites

Ensure you have the following installed on your machine:
- **Python** (v3.8 or higher)
- **Node.js** (v18 or higher) & **npm**
- **PostgreSQL** (running locally or via Docker)
- **Elasticsearch** (running locally or via Docker)

---

### 1️⃣ Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Set up the environment:**
    The project includes a `start.sh` script that automates the setup of the virtual environment and dependencies.
    ```bash
    ./start.sh
    ```
    *This script will create a virtual environment, install dependencies from `requirements.txt`, and start the FastAPI server.*

    **Manual Setup (Alternative):**
    ```bash
    # Create virtual environment
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Run the server
    python -m uvicorn app.main:app --reload
    ```

3.  **Environment Variables:**
    Create a `.env` file in the `backend` directory if required (refer to `app/core/config.py` for variables like `DATABASE_URL`, `ELASTICSEARCH_URL`).

    *Default API URL:* `http://localhost:8000`

---

### 2️⃣ Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```

4.  **Access the Application:**
    Open your browser and navigate to the URL provided by Vite (usually `http://localhost:5173`).

---

## 🛠️ Usage

1.  **Generate Logs**: Use the "Generate Logs" button on the dashboard to simulate user activity.
2.  **Train Model**: Click "Train Model" to update the anomaly detection model with the latest data.
3.  **Analyze Logs**: Run "Analyze Logs" to detect threats in the generated data.
4.  **Simulate Attack**: Use "Simulate Attack" to create synthetic malicious patterns and test system response.
5.  **View Alerts**: Check the dashboard for real-time risk scores, alerts, and detailed threat analysis.

## 🤝 Contribution

Feel free to contribute by submitting issues or pull requests. Please ensure you follow the project's coding standards.
