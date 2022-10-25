import time
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from src.operations.pause_until_loaded import pause_until_loaded


def input_speed_requested(driver, a, speed):
    # inputing the "speed requested"
    try:
        speed_requested_tab = Select(driver.find_element(
            By.XPATH, "(//div[@class='partnerHomeContent'])[3]//select"))
        if speed == 50:
            speed_requested_tab.select_by_visible_text("50Mbps and above")
        elif speed == 30:
            speed_requested_tab.select_by_visible_text("30Mbps and above")

        check_coverage_button = driver.find_element(
            By.XPATH, "//input[@type='image' and @value='Next' and @alt='submit']")
        a.move_to_element(check_coverage_button).click().perform()
        (driver, a) = pause_until_loaded(driver, a)
    except NoSuchElementException:
        driver.refresh()
        (driver, a) = pause_until_loaded(driver, a)
        input_speed_requested(driver, a, speed)
