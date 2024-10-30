import requests  # pip install requests
import pytz
from datetime import datetime
import json
from dotmap import DotMap  # pip install dotmap

COOKIES_PATH = 'appdata/cookies.json'


# 한국 시간을 기반으로 현재 타임스탬프를 밀리초로 반환
def timestamp():
    korea_timezone = pytz.timezone('Asia/Seoul')  # 한국 시간대 설정
    current_time = datetime.now(korea_timezone)  # 현재 한국 시간을 가져옴
    return int(current_time.timestamp() * 1000)  # 초를 밀리초로 변환


# 세션 설정
def set_session(cookies_str):
    try:
        cookies_list = json.loads(cookies_str)
        session = requests.Session()
        for cookie in cookies_list:
            session.cookies.set(cookie['name'], cookie['value'])
        return session
    except Exception as e:
        print(f'set_session error: {e}')
        return None


# 파일 읽기
def read_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf8') as f:
            result = f.read()
        return result
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None


# API 호출
def get_commute(emp_id, start_date, end_date):
    cookies = read_file(COOKIES_PATH)
    if not cookies:
        return False

    session = set_session(cookies)
    if not session:
        return False

    try:
        headers = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }
        params = {
            'empId': emp_id,
            'fromDate': start_date,
            'toDate': end_date,
            'chkWorkingDay': 'N',
            '_': timestamp()
        }
        response = session.get(
            'https://cowave.ncpworkplace.com/user/commute-status/list',
            params=params,
            headers=headers,
        )
        return DotMap(response.json())
    except Exception as exception:
        print(f"send error: {exception}")
        return False


def get_emp_id(email):
    cookies = read_file(COOKIES_PATH)
    if not cookies:
        return False

    session = set_session(cookies)
    if not session:
        return False

    headers = {
        'Referer': 'https://contact.worksmobile.com/v2/organization/chart',
    }
    params = {'keyword': email}
    response = session.get(
        'https://contact.worksmobile.com/v2/domain/contacts',
        params=params,
        headers=headers)
    if len(response.json()) == 0:
        raise Exception('No employee found.')
    res = DotMap(response.json()[0])
    return res.externalKey
