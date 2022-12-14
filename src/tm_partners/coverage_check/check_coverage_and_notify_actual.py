import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from src.tm_partners.operations.pause_until_loaded import pause_until_loaded
from src.tm_partners.db_read_write.db_write_address import write_or_edit_result

from src.tm_partners.singleton.current_db_row import CurrentDBRow
from src.tm_partners.coverage_check.input_speed_requested import input_speed_requested
from src.tm_partners.operations.login import Login
from src.tm_partners.singleton.retry_at_end import RetryAtEndCache
from ..operations.go_back_to_search_page import go_back_to_coverage_search_page


def check_coverage_and_notify_actual(driver, a):
    current_db_row = CurrentDBRow.get_instance()
    current_row_id = current_db_row.get_id(
        self=current_db_row)
    current_row_notify_email = current_db_row.get_notify_email(
        self=current_db_row)

    try:
        (driver, a) = pause_until_loaded(driver, a)
        WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div[4]/center/div[2]/div[2]/div/table/tbody/tr[2]/td/div[2]/div/form/div[3]/div[1]/table/tbody/tr[2]/td[1]/img[contains(@src, 'tick_checkcoverage')]")))
        # the green check mark is available.
        # result_text = ""
        # coverage_result = driver.find_element(
        #     By.XPATH, "//td[@align='justify']")
        # result_text = coverage_result.text
        # if "within the serviceable area" in result_text.lower():

        # handling edge case where there is an existing order error
        try:
            (driver, a) = pause_until_loaded(driver, a)
            WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div[4]/center/div[2]/div[2]/div/table/tbody/tr[2]/td/div[2]/div/form/div[3]/div[2]/table[2]")))
            addn_info = ' Has an existing order.'
        except TimeoutException:
            addn_info = ''

        # print("RESULT: is within servicable area")
        return ((current_row_id, 1, "Is within serviceable area!" + addn_info))

        # print("we're in the block where the green check mark is not available")

        # return go_back_to_coverage_search_page(driver, a)

    except TimeoutException:
        # red cross available. no green check mark.
        try:
            result_text = driver.find_element(
                By.XPATH, "//td//font[@color='red']").text
            if 'unable to process order. another progressing order created on the same address has been detected.' in result_text.lower():
                # print(
                # 'RESULT: unable to process order. another progressing order created on the same address has been detected.')
                return ((current_row_id, 6, "Another progressing order is created on the same address."))
                # send_message(
                #     address_string + "\nAnother progressing order created on the same address has been detected!")
                # send_email(
                # address_string + "\nAnother progressing order created on the same address has been detected!")
                # return go_back_to_coverage_search_page(driver, a)

        except NoSuchElementException:
            try:
                result_text = ""
                coverage_result = driver.find_element(
                    By.XPATH, "//td[@align='justify']")
                result_text = coverage_result.text

                if "cannot proceed with transfer request. service provider not the same with transfer request." in result_text.lower() or "due to create transfer request is required" in result_text.lower():
                    # print('RESULT: service provider not the same with transfer request.')
                    return ((current_row_id, 5, "Service provider not the same with Transfer Request."))
                    # send_message(
                    #     address_string + "\nService provider not the same with Transfer Request!")
                    # send_email(
                    # address_string + "\nService provider not the same with Transfer Request!")
                    # return go_back_to_coverage_search_page(driver, a)

                elif "is not within the serviceable area" in result_text.lower():
                    # print("RESULT: is not within the servicable area.")
                    return ((current_row_id, 4, "Not within serviceable area."))
                    # send_message(address_string +
                    #              "\nIs not within the servicable area!")
                    # send_email(address_string + "\nIs not within servicable area!")
                    # return go_back_to_coverage_search_page(driver, a)

                else:
                    return ((current_row_id, 7, "Other Error."))

            except NoSuchElementException:

                return ((current_row_id, 7, "Other Error."))

                # return go_back_to_coverage_search_page(driver, a)
