import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.tm_partners.singleton.current_db_row import CurrentDBRow
from src.tm_partners.singleton.selected_table_row import SelectedTableRow
from src.tm_partners.operations.send_in_correct_unit_num import preprocess_unit_num


def filter_unit_num(driver, a):
    unit_no_filter_tab = driver.find_element(
        By.XPATH, "//input[@id='flt0_resultAddressGrid' and @type='text' and @class='flt']")
    unit_no_filter_tab.clear()
    unit_no_filter_tab.send_keys(preprocess_unit_num())

    # number_of_results = len(driver.find_elements(
    # By.XPATH, "//tr[@class='odd' or @class='even'][not(@style)]"))
    number_of_results = len(driver.find_elements(
        By.XPATH, "//tr[@class='odd' or @class='even'][@style='']"))

    if number_of_results == 0:
        number_of_results = len(driver.find_elements(
            By.XPATH, "//tr[@class='odd' or @class='even'][not(@style)]"))

    if number_of_results == 0:
        # we should add the word "LOT" to the search string, and try again.
        unit_no_filter_tab = driver.find_element(
            By.XPATH, "//input[@id='flt0_resultAddressGrid' and @type='text' and @class='flt']")
        unit_no_filter_tab.clear()
        current_db_row = CurrentDBRow.get_instance()
        unit_no_filter_tab.send_keys("LOT " + preprocess_unit_num())

    number_of_results = len(driver.find_elements(
        By.XPATH, "//tr[@class='odd' or @class='even'][@style='']"))

    if number_of_results == 0:
        number_of_results = len(driver.find_elements(
            By.XPATH, "//tr[@class='odd' or @class='even'][not(@style)]"))

    if number_of_results == 0:
        selected_table_row_instance = SelectedTableRow.get_instance()
        selected_table_row_instance.set_lotnumfound(
            self=selected_table_row_instance, lotnumfound=False)
    else:
        selected_table_row_instance = SelectedTableRow.get_instance()
        selected_table_row_instance.set_lotnumfound(
            self=selected_table_row_instance, lotnumfound=True)

    return (driver, a)

def reset_unit_num_filter(driver, a):
    unit_no_filter_tab = driver.find_element(
        By.XPATH, "//input[@id='flt0_resultAddressGrid' and @type='text' and @class='flt']")
    unit_no_filter_tab.clear()
    unit_no_filter_tab.send_keys(Keys.BACKSPACE)

    return (driver, a)
