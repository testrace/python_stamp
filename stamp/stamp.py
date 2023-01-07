import sys

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def exception_exit(wd: webdriver, message):
    print(message)
    wd.quit()
    sys.exit(1)


options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

# 속도 향상을 위한 옵션 해제
prefs = {
    'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2, 'geolocation': 2,
                                               'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                               'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                               'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                                               'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                               'push_messaging': 2, 'ssl_cert_decisions': 2,
                                               'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                                               'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=options)

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"

stamp_url = "https://www.autowash.co.kr/event/attend_stamp.php?sno=3"
driver.get(stamp_url)

wait = WebDriverWait(driver, 10)

try:
    stamp_button = wait.until(
        expected_conditions.element_to_be_clickable((By.ID, 'attendanceCheck'))
    )
    print("출석페이지 이동 성공")
    stamp_button.click()
except TimeoutException:
    exception_exit(driver, "출석체크 버튼 없음")

try:
    wait.until(expected_conditions.alert_is_present())
    alert = driver.switch_to.alert
    print('alert message: ' + alert.text)
    alert.accept()
    print("로그인 페이지로 이동")
except TimeoutException:
    exception_exit(driver, "로그인 페이지 이동 alert 안뜸")

try:
    login_button = wait.until(
        expected_conditions.element_to_be_clickable((By.CLASS_NAME, 'member_login_order_btn'))
    )
    print("로그인 페이지 이동 성공")
    driver.execute_script("document.getElementById('loginId').value='loginId'")
    driver.execute_script("document.getElementById('loginPwd').value='loginPw'")
    login_button.click()
except TimeoutException:
    exception_exit(driver, "로그인 페이지 이동 실패")

try:
    stamp_button = wait.until(
        expected_conditions.element_to_be_clickable((By.ID, 'attendanceCheck'))
    )
    print("출석 버튼 클릭 성공")
    stamp_button.click()
except TimeoutException:
    exception_exit(driver, "로그인 후 출석체크 페이지 이동 실패(출석버튼 없음)")

try:
    wait.until(expected_conditions.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
except TimeoutException:
    print("출석 실패")
finally:
    driver.quit()
    sys.exit()
