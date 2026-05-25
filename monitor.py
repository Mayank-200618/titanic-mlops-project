import requests
import time
import os
from datetime import datetime
TARGET_URL = "http://localhost:5000/health"
MONITOR_LOG = "service_monitor.log"
print(f" Initializing active background health daemon against target endpoint:
{TARGET_URL}")
print("Checking status loop started. Output streaming to local text log files...")
while True:
 current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 try:
 execution_start = time.time()
 api_response = requests.get(TARGET_URL, timeout=4)
 latency_ms = (time.time() - execution_start) * 1000
 if api_response.status_code == 200:
 status_summary = f"[{current_time}] Operational - Code:
{api_response.status_code} - Latency: {latency_ms:.1f}ms"
 else:
 status_summary = f"[{current_time}] Anomaly - Unexpected HTTP Status:
{api_response.status_code}"
 except requests.exceptions.RequestException as network_error:
 status_summary = f"[{current_time}] Critical Alarm - offline - Error:
{str(network_error)}"
 print(status_summary)
 with open(MONITOR_LOG, "a") as file_stream:
 file_stream.write(status_summary + "\n")
 time.sleep(10)
