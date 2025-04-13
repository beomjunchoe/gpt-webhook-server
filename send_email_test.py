# send_email_test.py

import smtplib
from email.mime.text import MIMEText

msg = MIMEText("이건 테스트입니다. GPT 서버가 정상 작동 중입니다.")
msg['Subject'] = "GPT 테스트 메일"
msg['From'] = "lobfuehrer@gmail.com"
msg['To'] = "saintcamel@naver.com"

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login("lobfuehrer@gmail.com", "tbqxbfaqsythmfnc")
    server.send_message(msg)

print("메일 전송 완료!")
