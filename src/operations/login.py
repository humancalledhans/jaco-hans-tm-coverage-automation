# login('DPSL9701', 'Djns513!!', driver)

from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains

import time

from src.coverage_check.coverage_check import FindingCoverage
from src.operations.solve_captcha import solve_captcha


class Login:

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def login(self):

        username = self.username
        password = self.password

        proceed = False
        count = 0
        while not proceed:
            try:
                s = Service(ChromeDriverManager().install())
                options = Options()
                options.headless = False
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--force-device-scale-factor=1')
                options.add_argument("--no-sandbox")
                driver = webdriver.Chrome(service=s, options=options)
                driver.get('https://partners.unifi.my/HSBBPartnerPortal/HSBBPartnerPortal.portal?_nfpb=true&_pageLabel=login_portal&_nfls=false#wlp_HSBBPartnerPortal_portal_HelpCustomer/')
                while driver.execute_script("return document.readyState;") != "complete":
                    time.sleep(0.5)

                a = ActionChains(driver)

                user_name_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "//input[@type='text' and @id='portal.actionForm_username']")))
                user_name_field.clear()
                user_name_field.send_keys(username)

                password_field = driver.find_element(
                    By.XPATH, "//input[@type='password' and @id='portal.actionForm_password']")
                password_field.clear()
                password_field.send_keys(password)

                to_proceed = False
                while to_proceed == False:
                    captcha_to_solve = driver.find_element(
                        By.XPATH, "//img[@border='1' and @style='width: 220px;']")
                    captcha_code = solve_captcha(
                        captcha_elem_to_solve=captcha_to_solve, driver=driver)
                    while driver.execute_script("return document.readyState;") != "complete":
                        time.sleep(0.5)
                    captcha_field = WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                        (By.XPATH, "//input[@type='text' and @id='portal.actionForm_captchaCode']")))
                    captcha_field.clear()
                    captcha_field.send_keys(captcha_code)

                    login_button = driver.find_element(
                        By.XPATH, "//input[@type='image' and @alt='Login']")
                    a.move_to_element(login_button).click().perform()

                    try:
                        while driver.execute_script("return document.readyState;") != "complete":
                            time.sleep(0.5)
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                            (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

                    except TimeoutException:
                        to_proceed = True

                proceed = True

            except TimeoutException:
                count += 1
                # print(
                # "Unable to access page. Trying again automatically in 15 seconds...")
                # driver.close()
                # print("GET THE XCODE PATH OF THE MAINTENANCE PAGE!")
                # time.sleep(1500)
                # print("15 seconds has passed. Trying Again...")

                if count == 5:
                    # print("We tried for 5 times. Skipping...")
                    count = 0

        try:
            driver.find_element(
                By.XPATH, "//input[@type='image' and @alt='Login']")
            a.move_to_element(login_button).click().perform()

        except NoSuchElementException:
            finding_coverage = FindingCoverage()
            finding_coverage.finding_coverage(driver=driver, a=a)
