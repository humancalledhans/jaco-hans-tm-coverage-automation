from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

import time
from src.tm_partners.operations.pause_until_loaded import pause_until_loaded

from src.tm_partners.coverage_check.input_speed_requested import input_speed_requested


def go_back_to_coverage_search_page(driver, a):
    a.move_to_element(driver.find_element(
        By.XPATH, "(//div[@class='wlp-bighorn-window-content']//table//td//a)[1]")).click().perform()
    (driver, a) = input_speed_requested(driver, a, 50)
    (driver, a) = pause_until_loaded(driver, a)

    try:
        WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
            (By.XPATH, "//select[@id='actionForm_state']")))
        WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
            (By.XPATH, "//select[@id='actionForm_state']")))
        return (driver, a)

    except TimeoutException:
        go_back_to_coverage_search_page(driver, a)
