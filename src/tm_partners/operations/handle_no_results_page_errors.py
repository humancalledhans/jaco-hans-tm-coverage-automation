from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from src.tm_partners.operations.pause_until_loaded import pause_until_loaded

from src.tm_partners.singleton.current_db_row import CurrentDBRow
from src.tm_partners.operations.website_under_maintenance_wait import website_under_maintenance_wait
from ..operations.go_back_to_search_page import go_back_to_coverage_search_page

import time


def handle_no_results_page_errors(driver, a):
    try:
        a.move_to_element(driver.find_element(
            By.XPATH, "(//div[@class='wlp-bighorn-window-content']//div[@class='errorDisplay']//td//b)[1]")).click().perform()
        (driver, a) = pause_until_loaded(driver, a)

    except NoSuchElementException:
        current_db_row = CurrentDBRow.get_instance()

        try:
            (driver, a) = website_under_maintenance_wait(driver, a)

        except TimeoutException:

            print("ID ", current_db_row.get_id(
                self=current_db_row))
            print("HANS - FIND OUT WHAT YOU CAN DO! ITS A PROBLEM!")
            try:
                WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='subContent']//table//tbody//font[@color='red' and contains(text(), 'System unable to process the selected address due to technical issue.')]")))
                a.move_to_element(
                    driver.find_element(By.XPATH, ""))

            except TimeoutException:
                try:
                    WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                        (By.XPATH, "//td[@align='justify' and contains(text(), 'Sorry, the address in our database is incomplete based on your inputs.')]")))
                    # raise error in cvg_log.
                except TimeoutException:
                    print(
                        "HANS - WE'RE NOT IN THE SYSTEM UNABLE TO PROCESS ADRESS ERROR PAGE.")
                    time.sleep(300)
                    go_back_to_coverage_search_page(driver, a)
        except Exception as e:
            print(e)
            print("HANS - FIND OUT WHAT YOU CAN DO! ITS A PROBLEM!")
            time.sleep(300)
            go_back_to_coverage_search_page(driver, a)

    return (driver, a)
