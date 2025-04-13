import os
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

# 📌 주간 리포트용 라우트
@app.route("/weekly-report", methods=["GET"])
def weekly_report():
    try:
        with open("logs.txt", "r", encoding="utf-8") as f:
            logs = f.read()

        if not logs.strip():
            return jsonify({"status": "no logs"}), 200

        subject = "[WEEKLY REPORT] GPT 서버 이벤트 요약"
        send_email(subject, logs)

        # 로그 초기화
        open("logs.txt", "w").close()

        return jsonify({"status": "sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 📌 이벤트 수신 라우트
@app.route('/log-event', methods=['POST'])
def receive_log():
    data = request.json
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = f"[{now}] EVENT: {data}\n"
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(log_line)

    # 📍 심각도 자동 분류
    severity = "medium"  # 기본값
    payload = str(data).lower()

    if "lobfuehrer" in payload:
        severity = "unauthorized"
    elif any(p in payload for p in ["saintcamel", "01068051606"]):
        severity = "high"
    elif any(p in payload for p in ["범준", "개발자", "널 만들었어", "너 만든 사람"]):
        severity = "medium"

    # 📍 조건 충족 시 이메일 전송
    if severity in ["high", "unauthorized"]:
        subject = f"[ALERT:{severity.upper()}] GPT 보안 이벤트 발생 - {now}"
        body = f"다음과 같은 이벤트가 발생했습니다:\n\n{data}"
        send_email(subject, body)

    return jsonify({"status": "received"}), 200

@app.route("/", methods=["GET"])
def home():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
