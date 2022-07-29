import time
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select


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
        while driver.execute_script("return document.readyState;") != "complete":
            time.sleep(0.5)
    except NoSuchElementException:
        driver.refresh()
        while driver.execute_script("return document.readyState;") != "complete":
            time.sleep(0.5)
        input_speed_requested(driver, a, speed)
