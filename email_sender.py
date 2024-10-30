import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv  # pip install python-dotenv


class EmailSender:

    def __init__(self):
        # .env 파일을 로드
        load_dotenv()

        # .env에서 환경 변수를 불러옴
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.app_password = os.getenv("APP_PASSWORD")
        self.server = None

    def connect(self):
        try:
            # SMTP 서버에 연결
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.starttls()  # 보안 연결(STARTTLS)
            # 로그인
            self.server.login(self.sender_email, self.app_password)
            print("Connected to SMTP server.")
        except Exception as e:
            print(f"Failed to connect to SMTP server: {e}")
            if self.server:
                self.server.quit()

    def send_email(self, receiver_email, subject, body):
        try:
            # 이메일 내용 작성
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            # 본문 추가
            message.attach(MIMEText(body, "plain"))

            # 이메일 보내기
            text = message.as_string()
            self.server.sendmail(self.sender_email, receiver_email, text)

            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def disconnect(self):
        if self.server:
            self.server.quit()
            print("Disconnected from SMTP server.")
