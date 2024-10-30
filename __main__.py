from workalendar.asia import SouthKorea  # pip install workalendar
from datetime import datetime
import requests  # pip install requests
from email_sender import EmailSender
from calculate_rest_work_time.office_time_calculator import calculate_office_leave_time


# 한국 공휴일과 주말을 제외하고 이메일을 보내는 함수
def main():

    cal = SouthKorea()
    today = datetime.now().date()
    if cal.is_holiday(today) or today.weekday() >= 5:  # 주말 포함
        print("오늘은 주말 또는 공휴일입니다. 이메일을 보내지 않습니다.")
        return

    email_sender = EmailSender()
    email_sender.connect()
    notices = get_notices()
    for notice in notices:
        content = calculate_office_leave_time(notice["email"])
        email_sender.send_email(notice["email"], content, content)
    email_sender.disconnect()


# API 요청을 보내는 함수
def get_notices():
    url = 'http://localhost:8000/api/notices/'
    response = requests.get(url)
    return response.json()


if __name__ == "__main__":
    main()
