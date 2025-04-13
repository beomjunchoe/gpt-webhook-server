import requests
import json

url = "http://localhost:5001/log-event"

payload = {
    "timestamp": "2025-04-13T17:20:00Z",
    "event_type": "unauthorized_access_attempt",
    "trigger": "범준이야",
    "session_hash": "abc123xyz",
    "action": "응답 중단",
    "severity": "high"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print("응답 코드:", response.status_code)
print("응답 내용:", response.json())
