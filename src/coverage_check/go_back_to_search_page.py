from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

import time

from src.coverage_check.input_speed_requested import input_speed_requested


def go_back_to_coverage_search_page(driver, a):
    a.move_to_element(driver.find_element(By.XPATH, "(//div[@class='wlp-bighorn-window-content']//table//td//a)[1]")).click().perform()
    input_speed_requested(driver, a, 50)
    while driver.execute_script("return document.readyState;") != "complete":
        time.sleep(0.5)

    try:
        WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
            (By.XPATH, "//select[@id='actionForm_state']")))
        WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
            (By.XPATH, "//select[@id='actionForm_state']")))
        return

    except TimeoutException:
        go_back_to_coverage_search_page(driver,a)
