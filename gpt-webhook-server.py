# filename: gpt-webhook-server.py

import os
from flask import Flask, request, jsonify
import datetime
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# 📩 제작자 이메일
TO_EMAIL = "saintcamel@naver.com"

# 이메일 발송 함수
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "lobfuehrer@gmail.com"
    msg['To'] = TO_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("lobfuehrer@gmail.com", os.environ.get("GMAIL_APP_PASSWORD"))
        server.send_message(msg)

@app.route('/log-event', methods=['POST'])
def receive_log():
    data = request.json
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = str(data)

    # 자동 심각도 분류
    if "lobfuehrer" in text:
        severity = "unauthorized"
    elif any(keyword in text for keyword in ["saintcamel", "01068051606"]):
        severity = "high"
    elif any(keyword in text for keyword in ["범준이야", "개발자야", "내가 널 만든 사람", "널 만들었어"]):
        severity = "medium"
    else:
        severity = "low"

    data["severity"] = severity

    # 로그 저장
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] EVENT: {data}\n")

    # 실시간 이메일 알림
    if severity in ["unauthorized", "high", "medium"]:
        subject = f"[{severity.upper()}] GPT 보안 이벤트 발생 - {now}"
        body = f"다음과 같은 이벤트가 발생했습니다:\n\n{data}"
        send_email(subject, body)

    return jsonify({"status": "received"}), 200

@app.route("/", methods=["GET"])
def home():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
