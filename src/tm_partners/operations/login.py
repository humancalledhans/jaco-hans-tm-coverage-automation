# login('DPSL9701', 'Djns513!!', driver)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

from src.tm_partners.operations.enter_username_and_password import enter_username_and_password
from src.tm_partners.operations.driver_setup import driver_setup
from src.tm_partners.operations.pause_until_loaded import pause_until_loaded


from src.tm_partners.operations.solve_captcha import solve_captcha
from src.tm_partners.operations.set_accepted_params import set_accepted_params


class Login:

    def __init__(self):
        self.username = 'DPPJ1901'
        self.password = 'Dsync110!!'

        # self.username = 'DPSL3601'
        # self.password = 'Dptama201!'

    def login(self):

        username = self.username
        password = self.password

        proceed = False
        count = 0
        while not proceed:
            try:
                driver = driver_setup()
                driver.get('https://partners.unifi.my/HSBBPartnerPortal/HSBBPartnerPortal.portal?_nfpb=true&_pageLabel=login_portal&_nfls=false#wlp_HSBBPartnerPortal_portal_HelpCustomer/')
                a = ActionChains(driver)
                (driver, a) = pause_until_loaded(driver, a)
                (driver, a) = enter_username_and_password(
                    driver, a, username, password)

                to_proceed = False
                wait_iterations = 0
                while to_proceed == False:
                    captcha_to_solve = driver.find_element(
                        By.XPATH, "//img[@border='1' and @style='width: 220px;']")
                    captcha_code = solve_captcha(
                        captcha_elem_to_solve=captcha_to_solve, driver=driver)
                    (driver, a) = pause_until_loaded(driver, a)
                    captcha_field = WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                        (By.XPATH, "//input[@type='text' and @id='portal.actionForm_captchaCode']")))
                    captcha_field.clear()
                    captcha_field.send_keys(captcha_code)

                    login_button = driver.find_element(
                        By.XPATH, "//input[@type='image' and @alt='Login']")
                    a.move_to_element(login_button).click().perform()

                    try:
                        (driver, a) = pause_until_loaded(driver, a)
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                            (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))
                        wait_iterations += 1

                        if wait_iterations == 10:
                            driver.refresh()
                            wait_iterations = 0

                    except TimeoutException:
                        try:
                            WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                                (By.XPATH, "//input[@type='image' and @alt='Login']")))
                            login_button = driver.find_element(
                                By.XPATH, "//input[@type='image' and @alt='Login']")
                            a.move_to_element(login_button).click().perform()
                            (driver, a) = pause_until_loaded(driver, a)
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

        if proceed:
            return (driver, a)

        else:
            self.login()
