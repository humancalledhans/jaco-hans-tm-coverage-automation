from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
# from src.coverage_check.coverage_check import FindingCoverage
# from src.singleton.data_id_range import DataIdRange
from src.db_read_write.db_write_address import write_or_edit_result
from src.db_read_write.db_get_chat_id import get_chat_id

from src.singleton.current_input_row import CurrentInputRow
from src.notifications.telegram_msg import send_message
from src.notifications.email_msg import send_email
from .go_back_to_search_page import go_back_to_coverage_search_page

import time


def check_coverage_and_notify(table_row_num, driver, a, filtered):
    """
    this function accepts the best row's row number,
    1. checks the coverage, and 
    2. notifies the user.

    # NOTE: table_row_num starts at 0. that is, we assume that the first row is index 0 of the table, which is wrong.
    """

    def check_coverage_and_notify_actual(driver, a, address_string):
        current_input_row = CurrentInputRow.get_instance()
        current_row_id = current_input_row.get_id(
            self=current_input_row)
        current_row_notify_email = current_input_row.get_notify_email(
            self=current_input_row)

        try:
            while driver.execute_script("return document.readyState;") != "complete":
                time.sleep(0.5)
            WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div[4]/center/div[2]/div[2]/div/table/tbody/tr[2]/td/div[2]/div/form/div[3]/div[1]/table/tbody/tr[2]/td[1]/img[contains(@src, 'tick_checkcoverage')]")))
            # the green check mark is available.
            # result_text = ""
            # coverage_result = driver.find_element(
            #     By.XPATH, "//td[@align='justify']")
            # result_text = coverage_result.text
            # if "within the serviceable area" in result_text.lower():

            # print("RESULT: is within servicable area")
            write_or_edit_result(
                id=current_row_id, result_type=1, result_text="Is within serviceable area!")

            # print("we're in the block where the green check mark is not available")

            go_back_to_coverage_search_page(driver, a)
            return

        except TimeoutException:
            # red cross available. no green check mark.
            try:
                result_text = driver.find_element(
                    By.XPATH, "//td//font[@color='red']").text
                if 'unable to process order. another progressing order created on the same address has been detected.' in result_text.lower():
                    # print(
                    #     'RESULT: unable to process order. another progressing order created on the same address has been detected.')
                    write_or_edit_result(
                        id=current_row_id, result_type=6, result_text="Another progressing order is created on the same address.")
                    # send_message(
                    #     address_string + "\nAnother progressing order created on the same address has been detected!")
                    # send_email(
                    # address_string + "\nAnother progressing order created on the same address has been detected!")
                    go_back_to_coverage_search_page(driver, a)
                    return

            except NoSuchElementException:
                result_text = ""
                coverage_result = driver.find_element(
                    By.XPATH, "//td[@align='justify']")
                result_text = coverage_result.text

                if "cannot proceed with transfer request. service provider not the same with transfer request." in result_text.lower() or "due to create transfer request is required" in result_text.lower():
                    # print('RESULT: service provider not the same with transfer request.')
                    write_or_edit_result(
                        id=current_row_id, result_type=5, result_text="Service provider not the same with Transfer Request.")
                    # send_message(
                    #     address_string + "\nService provider not the same with Transfer Request!")
                    # send_email(
                    # address_string + "\nService provider not the same with Transfer Request!")
                    go_back_to_coverage_search_page(driver, a)
                    return

                elif "is not within the serviceable area" in result_text.lower():
                    # print("RESULT: is not within the servicable area.")
                    write_or_edit_result(
                        id=current_row_id, result_type=4, result_text="Not within serviceable area.")
                    # send_message(address_string +
                    #              "\nIs not within the servicable area!")
                    # send_email(address_string + "\nIs not within servicable area!")
                    go_back_to_coverage_search_page(driver, a)
                    return

                else:
                    write_or_edit_result(
                        id=current_row_id, result_type=7, result_text="Port full.")

                    go_back_to_coverage_search_page(driver, a)
                    return

    def bridge_to_actual_op(driver, a):
        address_string = ''
        current_input_row = CurrentInputRow.get_instance()
        input_house_unit_lotno = current_input_row.get_house_unit_lotno(
            self=current_input_row)
        input_street = current_input_row.get_street(self=current_input_row)
        input_section = current_input_row.get_section(self=current_input_row)
        input_floor_no = current_input_row.get_floor(self=current_input_row)
        input_building_name = current_input_row.get_building(
            self=current_input_row)
        input_city = current_input_row.get_city(self=current_input_row)
        input_state = current_input_row.get_state(self=current_input_row)
        input_postcode = current_input_row.get_postcode(self=current_input_row)

        if input_house_unit_lotno is None:
            input_house_unit_lotno = ''
        if input_street is None:
            input_street = ''
        if input_section is None:
            input_section = ''
        if input_floor_no is None:
            input_floor_no = ''
        if input_building_name is None:
            input_building_name = ''
        if input_city is None:
            input_city = ''
        if input_state is None:
            input_state = ''
        if input_postcode is None:
            input_postcode = ''

        address_string = address_string + \
            "House/Unit/Lot No." + input_house_unit_lotno + '\n' + \
            "Street: " + input_street + '\n' + \
            "Section: " + input_section + '\n' + \
            "Floor No: " + input_floor_no + '\n' + \
            "Building Name: " + input_building_name + '\n' + \
            "City: " + input_city + '\n' + \
            "State: " + input_state + '\n' + \
            "Postcode: " + input_postcode

        try:
            next_button = driver.find_element(
                By.XPATH, "//input[@type='image' and contains(@src, 'btnNext')]")
            a.move_to_element(next_button).click().perform()
            check_coverage_and_notify_actual(driver, a, address_string)
        except NoSuchElementException:
            # it means we're not at the "Type in more details" page.
            check_coverage_and_notify_actual(driver, a, address_string)

    # the implementation of the check_coverage_and_notify function starts here.
    # it calls bridge_to_actual_op() next, if there are no exceptions and problems.
    if not filtered:
        while driver.execute_script("return document.readyState;") != "complete":
            time.sleep(0.5)
        try:
            WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                (By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']")))

            x_code_path = "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"

        except TimeoutException:
            x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"

    else:
        x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]"

    select_button = driver.find_element(
        By.XPATH, f"({x_code_path})[{1+table_row_num}]//td//a//img")

    a.move_to_element(select_button).click().perform()
    while driver.execute_script("return document.readyState;") != "complete":
        time.sleep(0.5)

    try:
        # The page with "Sorry, we are unable to proceed at the moment. This error could be due to loss of connection to the server. Please try again later."
        driver.find_element(
            By.XPATH, "(//div[@class='errorDisplay']//div//table//b//text())[1]")
        link_to_click = driver.find_element(
            By.XPATH, "(//div[@class='errorDisplay']//div//table//tr//td//b//a)[1]")
        a.move_to_element(link_to_click).click().perform()

    except NoSuchElementException:

        try:
            while driver.execute_script("return document.readyState;") != "complete":
                time.sleep(0.5)

            # for when there is the "kindly fill in the missing information" page.
            WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='incompleteAddress']")))
            for missing_information in driver.find_elements(By.XPATH, "//input[@type='text']"):
                missing_information.send_keys("-")

            bridge_to_actual_op(driver, a)

        except TimeoutException:
            # for when there is NOT the "kindly fill in the missing information" page.
            while driver.execute_script("return document.readyState;") != "complete":
                time.sleep(0.5)

            try:
                WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                    (By.XPATH, "//table[@align='center' and @class='Yellow']")))
                bridge_to_actual_op(driver, a)

            except TimeoutException:
                try:
                    a.move_to_element(driver.find_element(
                        By.XPATH, "(//div[@class='wlp-bighorn-window-content']//div[@class='errorDisplay']//td//b)[1]")).click().perform()
                    while driver.execute_script("return document.readyState;") != "complete":
                        time.sleep(0.5)

                except NoSuchElementException:
                    print("HANS - FIND OUT WHAT YOU CAN DO! ITS A PROBLEM!")
                    time.sleep(300)

                # try:
                #     while driver.execute_script("return document.readyState;") != "complete":
                #         time.sleep(0.5)
                #     WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                #         (By.XPATH, "//table[@align='center' and @class='Yellow']")))
                #     bridge_to_actual_op(driver, a)

                # except TimeoutException:
                #     driver.execute_script("window.history.go(-1)")
                #     # TODO: figure out where this goes to.

                    # current_input_row = CurrentInputRow.get_instance()
                    # current_row_id = current_input_row.get_id(
                    #     self=current_input_row)
                    # data_id_range = DataIdRange.get_instance()
                    # data_id_end = data_id_range.get_end_id(
                    #     self=data_id_range)
                    # finding_coverage = FindingCoverage.get_instance()
                    # finding_coverage.finding_coverage(
                    #     driver, a, data_id_start=current_row_id, data_id_end=data_id_end)
