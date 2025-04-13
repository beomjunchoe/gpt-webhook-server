# filename: webhook_server.py

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
    server.login("lobfuehrer@gmail.com", "tbqxbfaqsythmfnc")

@app.route('/log-event', methods=['POST'])
def receive_log():
    data = request.json
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 로그 저장
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] EVENT: {data}\n")

    # 실시간 경고 조건
    if data.get("severity") == "high":
        subject = f"[ALERT] GPT 보안 이벤트 발생 - {now}"
        body = f"다음과 같은 이벤트가 발생했습니다:\n\n{data}"
        send_email(subject, body)

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(port=5001)

@app.route("/", methods=["GET"])
def home():
    return {"status": "ok"}