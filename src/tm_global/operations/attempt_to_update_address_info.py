import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def attempt_to_update_address_information(driver, a):

    (driver, a) = pause_until_loaded(driver, a)
    try:
        overlay_content = WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='modal-content']")))

        a.move_to_element(overlay_content).click().perform()

        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='modal-content']//input[@type='text' and @id='readonly_house_unit_lot']")))

        hse_unit_no_required_field = driver.find_element(
            By.XPATH, "//div[@class='modal-content']//input[@type='text' and @id='readonly_house_unit_lot']")
        hse_unit_no_required_field.clear()
        hse_unit_no_required_field.send_keys('-')

        confirm_btn = driver.find_element(
            By.XPATH, "//button[@class='btn btn-blue-white w-350px' and contains(text(), 'YES, CONFIRM IT')]")
        a.move_to_element(confirm_btn).click().perform()
        (driver, a) = pause_until_loaded(driver, a)
        return (driver, a)

    except NoSuchElementException:
        return (driver, a)
