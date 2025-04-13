import os
import uuid
from flask import Flask, request, jsonify
import datetime
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
TO_EMAIL = "saintcamel@naver.com"

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "lobfuehrer@gmail.com"
    msg['To'] = TO_EMAIL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("lobfuehrer@gmail.com", os.environ.get("GMAIL_APP_PASSWORD"))
        server.send_message(msg)

@app.route("/weekly-report", methods=["GET"])
def weekly_report():
    try:
        with open("logs.txt", "r", encoding="utf-8") as f:
            logs = f.read()

        if not logs.strip():
            return jsonify({"status": "no logs"}), 200

        subject = "[WEEKLY REPORT] GPT 서버 이벤트 요약"
        send_email(subject, logs)

        open("logs.txt", "w").close()
        return jsonify({"status": "sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/log-event', methods=['POST'])
def receive_log():
    data = request.json
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 자동 session_hash 생성
    session_hash = str(uuid.uuid4())
    data["session_hash"] = session_hash

    # 심각도 자동 분류
    payload = str(data).lower()
    severity = "medium"
    if "lobfuehrer" in payload:
        severity = "unauthorized"
    elif any(p in payload for p in ["saintcamel", "01068051606", "시윤", "태윤", "라윤"]):
        severity = "high"
    elif any(p in payload for p in ["범준", "개발자", "널 만들었어", "너 만든 사람", "사랑해", "서혜", "채은"]):
        severity = "medium"

    data["severity"] = severity

    # 로그 저장
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] EVENT: {data}\n")

    # 이메일 발송
    if severity in ["high", "unauthorized"]:
        subject = f"[ALERT:{severity.upper()}] GPT 보안 이벤트 발생 - {now}"
        body = f"다음과 같은 이벤트가 발생했습니다:\n\n{data}"
        send_email(subject, body)

    return jsonify({"status": "received", "session_hash": session_hash}), 200

@app.route("/", methods=["GET"])
def home():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
