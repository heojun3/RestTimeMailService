import json
from func_timeout import func_set_timeout
from .selenium_helpers import (initialize_browser, wait_for_element_by_id,
                               perform_login, get_error_message,
                               retrieve_cookies, close_browser)


# 파일 저장 함수
def save_to_file(file_name, data):
    with open(file_name, 'w', encoding='utf8') as f:
        f.write(data)
    return 200


# 로그인 수행 및 상태 확인 함수
@func_set_timeout(60)
def attempt_login(driver, email, password):
    driver.get(
        'https://auth.worksmobile.com/login/login?accessUrl=http%3A%2F%2Fcowave.ncpworkplace.com%2Fv%2Fhome%2F'
    )

    try:
        if not wait_for_element_by_id(driver, 'user_id'):
            raise Exception('Login page not loaded')
        if not perform_login(driver, email, password):
            raise Exception('Login failed')
        if not wait_for_element_by_id(driver, 'workplaceLayer'):
            raise Exception('Main page not loaded')
        return True
    except Exception as err:
        print(f'Login process failed: {err}')
        return get_error_message(driver) if 'Main page' in str(err) else False


# 로그인 후 쿠키 업데이트 함수
def save_login_cookie(email, password):
    driver = initialize_browser()
    login_success = attempt_login(driver, email, password)

    if login_success is True:
        cookies = retrieve_cookies(driver)
        save_to_file('appdata/cookies.json', json.dumps(cookies))
        print("로그인 및 쿠키 저장 성공")
    else:
        print(f"로그인 실패: {login_success}")
    close_browser(driver)
