import sys

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()

driver.get("https://www.autowash.co.kr/member/login.php")
driver.maximize_window()

try:
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "member_login_order_btn"))
    )
finally:
    print("로그인 페이지 이동")

inputId = driver.find_element(By.ID, "loginId")
inputId.send_keys("id")

inputPw = driver.find_element(By.ID, "loginPwd")
inputPw.send_keys("pw")

driver.find_element(By.CLASS_NAME, "member_login_order_btn").click()
driver.implicitly_wait(5)

try:
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.LINK_TEXT, '로그아웃'))
    )
finally:
    print("로그인 성공")

stamp_url = "https://www.autowash.co.kr/event/attend_stamp.php?sno=3"
driver.get(stamp_url)

try:
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.ID, 'attendanceCheck'))
    )
finally:
    print("출석페이지 이동 성공")
    driver.implicitly_wait(5)
    stamp_button = driver.find_element(By.ID, "attendanceCheck")
    stamp_button.click()

try:
    WebDriverWait(driver, 10).until(expected_conditions.alert_is_present())
    alert = driver.switch_to.alert
    print(alert.text)
    alert.accept()
    driver.quit()
    sys.exit()
except TimeoutException:
    print("출석 끝")

driver.quit()
sys.exit()
