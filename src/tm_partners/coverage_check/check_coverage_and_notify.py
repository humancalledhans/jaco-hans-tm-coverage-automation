import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from src.tm_partners.operations.detect_and_solve_captcha import detect_and_solve_captcha
from src.tm_partners.operations.pause_until_loaded import pause_until_loaded

from src.tm_partners.coverage_check.bridge_to_actual_op import bridge_to_actual_op
from src.tm_partners.operations.wait_to_decide_xpath import wait_to_decide_xpath
from src.tm_partners.operations.we_are_not_able_to_proceed_error import we_are_not_able_to_proceed_error
from src.tm_partners.operations.kindly_fill_in_missing_info_page import kindly_fill_in_missing_info_page
from src.tm_partners.operations.handle_no_results_page_errors import handle_no_results_page_errors
from src.tm_partners.operations.driver_setup import driver_setup
from src.tm_partners.operations.arrive_at_results_page import arrive_at_results_page


def check_coverage_and_notify(table_row_num, driver, a, filtered):
    """
    this function accepts the best row's row number,
    1. checks the coverage (by clicking on 'select'), and 
    2. notifies the user.

    # NOTE: table_row_num starts at 0. that is, we assume that the first row is index 0 of the table, which is wrong.
    """

    # it calls bridge_to_actual_op() next, if there are no exceptions and problems.
    if not filtered:
        (driver, a) = pause_until_loaded(driver, a)
        x_code_path = wait_to_decide_xpath(driver, a)

    else:
        x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]"

    try:
        link_to_check = driver.find_element(
            By.XPATH, f"({x_code_path})[{1+table_row_num}]//td//a").get_attribute('href')
    except NoSuchElementException:
        x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style='display: none;')]" 
        link_to_check = driver.find_element(
            By.XPATH, f"({x_code_path})[{1+table_row_num}]//td//a").get_attribute('href')

    driver.execute_script("window.open('');")

    # Switch to the new window and open new URL
    driver.switch_to.window(driver.window_handles[1])
    driver.get(link_to_check)
    (driver, a) = pause_until_loaded(driver, a)

    (driver, a) = arrive_at_results_page(driver, a)

    return (driver, a)
