import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from google import genai
from dotenv import load_dotenv
import warnings

# Suppress sklearn warnings for cleaner output
warnings.filterwarnings("ignore")

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("API Key not found. Please set GEMINI_API_KEY in your .env file.")

def generate_synthetic_logs(num_logs=500):
    """Generates normal network logs and injects a few anomalies."""
    print("[*] Generating synthetic network logs...")
    np.random.seed(42)
    
    # Normal traffic
    data = {
        'source_ip': [f"192.168.1.{np.random.randint(1, 100)}" for _ in range(num_logs)],
        'dest_port': np.random.choice([80, 443, 22, 53], size=num_logs, p=[0.5, 0.3, 0.1, 0.1]),
        'bytes_transferred': np.random.normal(5000, 1000, num_logs).astype(int),
        'failed_logins': np.random.choice([0, 1], size=num_logs, p=[0.95, 0.05])
    }
    df = pd.DataFrame(data)
    
    # Injecting an obvious attack pattern (Anomaly 1: Data Exfiltration)
    df.loc[10] = ['10.0.0.5', 443, 5000000, 0] 
    
    # Injecting another attack pattern (Anomaly 2: Brute Force)
    df.loc[42] = ['172.16.0.8', 22, 1500, 45] 
    
    return df

def detect_anomalies(df):
    """Uses Isolation Forest to detect anomalous logs."""
    print("[*] Training Isolation Forest model to detect anomalies...")
    features = ['dest_port', 'bytes_transferred', 'failed_logins']
    X = df[features]
    
    model = IsolationForest(contamination=0.01, random_state=42)
    df['anomaly_score'] = model.fit_predict(X)
    
    anomalies = df[df['anomaly_score'] == -1].drop(columns=['anomaly_score'])
    return anomalies

def generate_ai_triage_report(anomalous_data):
    """Sends the anomalous data to Gemini 3 for analysis using the new SDK."""
    print("[*] Sending anomalies to AI for Triage Report...\n")
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    You are an expert Tier 3 SOC Analyst. Review the following anomalous network logs detected by our machine learning model. 
    
    Log Data:
    {anomalous_data.to_string()}
    
    Provide a concise Threat Triage Report. For each unique source IP, specify:
    1. The likely type of attack or suspicious behavior occurring.
    2. A severity rating (Low, Medium, High, Critical).
    3. Recommended immediate remediation steps.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error communicating with AI API: {str(e)}"

if __name__ == "__main__":
    print("=== AI-Powered SOC Analyst Initialized (v2.0) ===\n")
    
    logs_df = generate_synthetic_logs()
    anomalies_df = detect_anomalies(logs_df)
    
    print(f"[*] Detected {len(anomalies_df)} anomalous events.")
    
    if not anomalies_df.empty:
        report = generate_ai_triage_report(anomalies_df)
        print("="*50)
        print("THREAT INTELLIGENCE REPORT")
        print("="*50)
        print(report)
    else:
        print("[*] No anomalies detected.")
