# AI-Powered SOC Analyst

An automated cybersecurity tool that uses Machine Learning (Isolation Forest) to detect network anomalies and Google's Gemini AI to generate professional Threat Triage Reports.

## Features
* **Synthetic Log Generation:** Simulates normal network traffic alongside injected attack patterns (Data Exfiltration, SSH Brute Force).
* **Machine Learning Detection:** Uses `scikit-learn`'s Isolation Forest to detect statistical outliers without relying on static rules.
* **AI Alert Triage:** Integrates with the `google-genai` SDK to evaluate flagged anomalies and output actionable remediation steps.

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

# Install requirements:

```Bash
pip install -r requirements.txt
```

# Run the script:

```Bash
python soc_analyst.py
```

# Sample Output:

``plaintext
=== AI-Powered SOC Analyst Initialized (v2.0) ===

[*] Generating synthetic network logs...
[*] Training Isolation Forest model to detect anomalies...
[*] Detected 5 anomalous events.
[*] Sending anomalies to AI for Triage Report...

==================================================
THREAT INTELLIGENCE REPORT
==================================================
### **Threat Triage Report**

**To:** SOC Manager / Incident Response Team
**From:** Tier 3 SOC Analyst
**Subject:** Triage of Anomalous Network Activity (ML-Detected)

---

#### **1. Source IP: 172.16.0.8**
* **Likely Attack Type:** **SSH Brute Force Attack.** The high volume of failed logins (45) on port 22 is a signature of automated credential stuffing or password guessing.
* **Severity:** **High**
* **Recommended Remediation:**
    1.  Immediately block the source IP at the perimeter firewall.
    2.  Verify if any successful logins occurred from this IP following the failures.
    3.  Force a password reset for any accounts targeted during this window.
    4.  Ensure SSH is restricted to VPN-only access and implement Key-Based Authentication.

#### **2. Source IP: 10.0.0.5**
* **Likely Attack Type:** **Potential Data Exfiltration / Unauthorized Data Transfer.** While no failed logins occurred, the byte count (5MB) is a significant outlier compared to baseline traffic on port 443. This may indicate a staged file upload or data "beaconing."
* **Severity:** **Medium**
* **Recommended Remediation:**
    1.  Identify the destination IP/Domain (not provided in this log slice) to determine if it is a known cloud storage provider or malicious C2.
    2.  Perform a host-level forensic scan to identify the process initiating the connection.
    3.  Review NetFlow logs for this host over the last 24 hours to check for recurring patterns of large transfers.

#### **3. Source IPs: 192.168.1.91, 192.168.1.44, 192.168.1.87**
* **Likely Attack Type:** **Likely False Positive / Minor User Error.** A single failed login on port 443 (HTTPS) with low data volume is consistent with a user mistyping a password on a web application.
* **Severity:** **Low**
* **Recommended Remediation:**
    1.  No immediate action required. 
    2.  Continue to monitor these IPs for a spike in `failed_logins` which could indicate the start of a web-based brute force attempt. 
    3.  Tune the ML model to ignore single-instance login failures to reduce alert fatigue.

---
**Analyst Note:** The activity from `172.16.0.8` is the priority. The host at `10.0.0.5` should be investigated immediately after the SSH threat is neutralized to ensure a data breach is not in progress.```
