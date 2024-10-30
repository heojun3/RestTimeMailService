from datetime import timedelta, datetime
from .api import get_emp_id, get_commute


# 남은 시간 계산
def calculate_rest_work_time(email):
    start_date, end_date = get_this_month_period()

    emp_id = get_emp_id(email)
    commutes = get_commute(emp_id, start_date, end_date)

    total_work_time = calculate_total_work_time(commutes)
    work_day = count_can_work_days(commutes)
    need_time = timedelta(hours=8 * work_day)

    today_need_time = timedelta(hours=8)  # 오늘 필요한 시간 (기본적으로 8시간)
    rest_work_time = total_work_time - (need_time - today_need_time)
    return format_timedelta(rest_work_time)


# 오늘 날짜 문자열 반환
def get_today_date_string():
    return datetime.now().strftime('%Y%m%d')


def get_this_month_period():
    now = datetime.now()
    start_of_month = now.replace(day=1)
    next_month = (now.replace(day=28) + timedelta(days=4))
    end_of_month = next_month - timedelta(days=next_month.day)

    start_date = start_of_month.strftime('%Y%m%d')
    end_date = end_of_month.strftime('%Y%m%d')

    return start_date, end_date


# 총 근무시간 계산
def calculate_total_work_time(data):
    work_times = []
    time_format = '%H%M'
    today = get_today_date_string()

    for d in data.data.list:
        if d.dayTpCd != 'WORK':
            continue

        real_in_time = safe_parse_time(d.realInHm, '0000', time_format)
        real_out_time = safe_parse_time(d.realOutHm, '0000', time_format)
        rest_time = safe_parse_time(d.restTime, '0000', time_format)
        absence_time = safe_parse_time(d.absenceTime, '0000', time_format)

        # 근무 시간 계산
        work_time = (real_out_time - real_in_time) + (absence_time - rest_time)
        work_times.append(max(work_time, timedelta(seconds=0)))

        if d.checkYmd == today:
            break

    return sum(work_times, timedelta())


# 안전한 시간 파싱
def safe_parse_time(time_str, default, time_format):
    try:
        return datetime.strptime(time_str if time_str else default,
                                 time_format)
    except ValueError:
        return datetime.strptime(default, time_format)


# 근무 가능한 일 수 계산
def count_can_work_days(data):
    count = 0
    today = get_today_date_string()

    for d in data.data.list:
        if d.dayTpCd == 'WORK' and d.standInHm:
            count += 1
        if d.checkYmd == today:
            break

    return count


# timedelta 포맷팅
def format_timedelta(td):
    hours, remainder = divmod(abs(td).seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if td.days < 0:
        return f"최소근무시간 기준 {hours}시간 {minutes}분 부족"
    return f"최소근무시간 기준 {hours}시간 {minutes}분 초과"
