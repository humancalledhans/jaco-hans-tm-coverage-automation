from src.tm_partners.singleton.current_input_row import CurrentInputRow
from src.tm_partners.singleton.data_id_range import DataIdRange
from src.tm_partners.operations.solve_captcha import solve_captcha
from src.tm_partners.operations.pause_until_loaded import pause_until_loaded

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


def detect_and_solve_captcha(driver, a):
    to_proceed = False
    while to_proceed == False:
        try:
            (driver, a) = pause_until_loaded(driver, a)
            captcha_to_solve = WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='blockUI blockMsg blockPage']//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[@src='jcaptchaCustom.jpg' and @border='1']")))
            captcha_code = solve_captcha(
                captcha_elem_to_solve=captcha_to_solve, driver=driver)
            # print("HERE2")
            captcha_field = driver.find_element(
                By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//input[@type='text']")
            captcha_field.clear()
            captcha_field.send_keys(captcha_code)
            submit_captcha_button = driver.find_element(
                By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[contains(@src, 'btnGo')]")
            a.move_to_element(
                submit_captcha_button).click().perform()

            try:
                (driver, a) = pause_until_loaded(driver, a)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                    (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

            except TimeoutException:
                to_proceed = True

        except TimeoutException:
            # print(
            #     "Retrying step FIVE - going back and comparing each address...")
            to_proceed = True
    return (driver, a)


def detect_and_solve_captcha_but_rerun(driver, a, finding_coverage_instance):
    to_proceed = False
    while to_proceed == False:
        try:
            (driver, a) = pause_until_loaded(driver, a)
            captcha_to_solve = WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='blockUI blockMsg blockPage']//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[@src='jcaptchaCustom.jpg' and @border='1']")))
            captcha_code = solve_captcha(
                captcha_elem_to_solve=captcha_to_solve, driver=driver)
            # print("HERE1")
            captcha_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//input[@type='text']")))
            captcha_field.clear()
            captcha_field.send_keys(captcha_code)
            submit_captcha_button = driver.find_element(
                By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[contains(@src, 'btnGo')]")
            a.move_to_element(submit_captcha_button).click().perform()

            try:
                (driver, a) = pause_until_loaded(driver, a)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                    (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

            except TimeoutException:
                to_proceed = True
                # break

        except TimeoutException:
            current_input_row = CurrentInputRow.get_instance()
            current_row_id = current_input_row.get_id(
                self=current_input_row)
            data_id_range = DataIdRange.get_instance()
            data_id_end = data_id_range.get_end_id(self=data_id_range)
            finding_coverage_instance.finding_coverage(
                driver, a, data_id_start=current_row_id, data_id_end=data_id_end)
            continue
