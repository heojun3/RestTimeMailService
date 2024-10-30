import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


# 브라우저 생성 함수
def initialize_browser():
    chrome_options = Options()
    driver = webdriver.Remote(
        command_executor='http://selenium-chrome:4444/wd/hub',
        options=chrome_options)
    return driver


# 특정 요소 대기 함수
def wait_for_element_by_id(driver, element_id, timeout=3):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, element_id)))
        return True
    except TimeoutException:
        print(
            f'Element with ID {element_id} not found within {timeout} seconds.'
        )
        return False


# 로그인 처리 함수
def perform_login(driver, email, password):
    try:
        email_input = driver.find_element(By.ID, 'user_id')
        email_input.send_keys(email)

        login_start_button = driver.find_element(By.ID, 'loginStart')
        login_start_button.click()

        time.sleep(1)

        password_input = driver.find_element(By.ID, 'user_pwd')
        password_input.send_keys(password)

        login_button = driver.find_element(By.ID, 'loginBtn')
        login_button.click()

        return True
    except NoSuchElementException:
        print('perform_login 에러: 요소를 찾을 수 없음')
        return False
    except Exception as e:
        print(f'perform_login 에러: {str(e)}')
        return False


# 에러 메시지 추출 함수
def get_error_message(driver):
    try:
        error_message_element = driver.find_element(By.ID, 'div_fail_message')
        return error_message_element.text
    except NoSuchElementException:
        return ''


# 쿠키 가져오기 함수
def retrieve_cookies(driver):
    return driver.get_cookies()


# 브라우저 종료 함수
def close_browser(driver):
    driver.quit()
