from unittest import result
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains

from current_input_row.current_input_row import CurrentInputRow

from notifications.telegram_msg import send_message
from notifications.email_msg import send_email
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
        try:
            while driver.execute_script("return document.readyState;") != "complete":
                time.sleep(0.5)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div[4]/center/div[2]/div[2]/div/table/tbody/tr[2]/td/div[2]/div/form/div[3]/div[1]/table/tbody/tr[2]/td[1]/img[contains(@src, 'tick_checkcoverage')]")))
            # the green check mark is available.
            result_text = ""
            coverage_result = driver.find_element(
                By.XPATH, "//td[@align='justify']")
            result_text = coverage_result.text
            if "within the serviceable area" in result_text.lower():
                print("RESULT: is within servicable area")
                send_message(address_string + "\nIs within serviceable area!")
                # send_email(address_string + "\nIs within serviceable area!")

            else:
                print("we're in the block where the green check mark is not available")
                result_text = driver.find_element(
                    By.XPATH, "//td//font[@color='red']").text
                if 'unable to process order. another progressing order created on the same address has been detected.' in result_text.lower():
                    print(
                        'RESULT: unable to process order. another progressing order created on the same address has been detected.')
                    # send_message(
                    #     address_string + "\nAnother progressing order created on the same address has been detected!")
                    # send_email(
                    # address_string + "\nAnother progressing order created on the same address has been detected!")

            go_back_to_coverage_search_page(driver)

        except TimeoutException:
            result_text = ""
            coverage_result = driver.find_element(
                By.XPATH, "//td[@align='justify']")
            result_text = coverage_result.text

            if "cannot proceed with transfer request. service provider not the same with transfer request." in result_text.lower():
                print('RESULT: service provider not the same with transfer request.')
                # send_message(
                #     address_string + "\nService provider not the same with Transfer Request!")
                # send_email(
                # address_string + "\nService provider not the same with Transfer Request!")

            elif "is not within the serviceable area" in result_text.lower():
                print("RESULT: is not within the servicable area.")
                # send_message(address_string +
                #              "\nIs not within the servicable area!")
                # send_email(address_string + "\nIs not within servicable area!")

            go_back_to_coverage_search_page(driver)

    def bridge_to_actual_op(driver, a):
        address_string = ''
        current_input_row = CurrentInputRow.get_instance()
        input_header_data = current_input_row.get_input_header_data(
            self=current_input_row)
        input_row_data = current_input_row.get_input_row_data(
            self=current_input_row)
        input_house_unit_lotno = current_input_row.get_house_unit_lotno(
            self=current_input_row)
        input_street_type = current_input_row.get_street_type(
            self=current_input_row)
        input_street_name = current_input_row.get_street_name(
            self=current_input_row)
        input_section = current_input_row.get_section(self=current_input_row)
        input_floor_no = current_input_row.get_floor_no(self=current_input_row)
        input_building_name = current_input_row.get_building_name(
            self=current_input_row)
        input_city = current_input_row.get_city(self=current_input_row)
        input_state = current_input_row.get_state(self=current_input_row)
        input_postcode = current_input_row.get_postcode(self=current_input_row)

        address_string = address_string + \
            "House/Unit/Lot No." + input_house_unit_lotno + '\n' + \
            "Street Type: " + input_street_type + '\n' + \
            "Street Name: " + input_street_name + '\n' + \
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
    if not filtered:
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']")))
            x_code_path = "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"

        except TimeoutException:
            x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"

    else:
        x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]"

    select_button = driver.find_element(
        By.XPATH, f"({x_code_path})[{1+table_row_num}]//td//a//img")  # NOTE TO HANS: KNOW THAT THIS WAS 3+table_row_num before.

    a.move_to_element(select_button).click().perform()
    try:
        while driver.execute_script("return document.readyState;") != "complete":
            time.sleep(0.5)

        # for when there is the "kindly fill in the missing information" page.
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='incompleteAddress']")))
        for missing_information in driver.find_elements(By.XPATH, "//input[@type='text']"):
            missing_information.send_keys("-")

        bridge_to_actual_op(driver, a)

    except TimeoutException:
        # for when there is NOT the "kindly fill in the missing information" page.
        while driver.execute_script("return document.readyState;") != "complete":
            time.sleep(0.5)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//table[@align='center' and @class='Yellow']")))
            bridge_to_actual_op(driver, a)

        except TimeoutException:
            time.sleep(300)  # this actually needs to be 300.
            driver.refresh()
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "//table[@align='center' and @class='Yellow']")))
                bridge_to_actual_op(driver, a)

            except TimeoutException:
                driver.execute_script("window.history.go(-1)")
                # TODO: figure out where this goes to.
