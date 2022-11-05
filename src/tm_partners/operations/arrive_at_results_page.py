from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from src.tm_partners.operations.detect_and_solve_captcha import detect_and_solve_captcha
from src.tm_partners.operations.pause_until_loaded import pause_until_loaded

from src.tm_partners.coverage_check.bridge_to_actual_op import bridge_to_actual_op
from src.tm_partners.operations.we_are_not_able_to_proceed_error import we_are_not_able_to_proceed_error
from src.tm_partners.operations.kindly_fill_in_missing_info_page import kindly_fill_in_missing_info_page
from src.tm_partners.operations.handle_no_results_page_errors import handle_no_results_page_errors


def arrive_at_results_page(driver, a):

    (driver, a) = detect_and_solve_captcha(driver, a)
    (driver, a) = pause_until_loaded(driver, a)

    try:
        (driver, a) = we_are_not_able_to_proceed_error(driver, a)

        (driver, a) = detect_and_solve_captcha(driver, a)

    except NoSuchElementException:
        try:
            (driver, a) = pause_until_loaded(driver, a)

            (driver, a) = kindly_fill_in_missing_info_page(driver, a)

        except TimeoutException:
            # for when there is NOT the "kindly fill in the missing information" page.
            (driver, a) = pause_until_loaded(driver, a)

            try:
                # yep, this is where we go in and check the coverage results.
                WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                    (By.XPATH, "//table[@align='center' and @class='Yellow']")))

            except TimeoutException:
                # the handle_no_results_page_errors() method returns (driver, a)
                # it goes back to the coverage_search_page, however.
                (driver, a) = handle_no_results_page_errors(driver, a)

    finally:
        return (driver, a)
