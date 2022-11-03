# login('DPSL9701', 'Djns513!!', driver)

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

from src.tm_global.operations.enter_username_and_password import enter_username_and_password
from src.tm_global.operations.tm_global_driver_setup import tm_global_driver_setup
from src.tm_global.operations.pause_until_loaded import pause_until_loaded

# from src.tm_global.coverage_check.coverage_check import FindingCoverage
from src.tm_global.operations.set_accepted_params import set_accepted_params
from src.tm_global.operations.click_on_login_btn import click_on_login_button


class TMGlobalLogin:

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def login(self, driver, a):

        username = self.username
        password = self.password

        logged_in = False
        count = 0
        while not logged_in:
            try:
                (driver, a) = pause_until_loaded(driver, a)
                (driver, a) = enter_username_and_password(
                    driver, a, username, password)

                try:
                    (driver, a) = click_on_login_button(driver, a)
                    logged_in = True

                except TimeoutException:
                    try:
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                            (By.XPATH, "//p[@class='f-red pt-3 pb-3' and contains(text(),'The user credentials were incorrect.')]")))
                    except TimeoutException:
                        print("UNABLE TO LOGIN.")

                logged_in = True

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

        if logged_in:
            return (driver, a)

        else:
            self.login()
