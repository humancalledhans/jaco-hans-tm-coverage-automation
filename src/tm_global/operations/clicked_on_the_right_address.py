import time
from src.tm_global.operations.get_coverage_result import get_coverage_result

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.operations.filter_all_columns import filter_all_columns
from src.tm_global.operations.click_on_selected_row import click_on_selected_row
from src.tm_global.operations.duplicate_in_new_tab import duplicate_in_new_tab
from src.tm_global.operations.close_duplicated_tab import close_duplicated_tab
from src.tm_global.operations.verify_to_click_on_row import verify_to_click_on_row
from src.tm_global.operations.restart_filter_process import restart_filter_process
from src.tm_global.singleton.selected_table_row import SelectedTableRow
from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.attempt_to_update_address_info import attempt_to_update_address_information


def coverage_search_the_right_address(driver, a, address):
    """
    'address' param would be in the form of:
    ((['61', 'JALAN', 'TANJUNG 2', 'BUKIT BERUNTUNG', '', '', 'SERENDAH', '48300', 'FTTH', 'Residential'],1), ('BEST MATCH', True))
    """
    address_marks = address[1][0]
    lotNumAndStreetAndPostcodeNumMatchBool = address[1][1]
    address_string = ''
    for str_idx in range(len(address[0][0])-2):
        if address[0][0][str_idx] != '' and address[0][0][str_idx] != ' ' and address[0][0][str_idx].strip() != '-':
            address_string += address[0][0][str_idx] + ' '

    address_string = address_string.strip()

    (driver, a) = filter_all_columns(driver, a, address)

    best_selection_row = driver.find_elements(
        By.XPATH, "//table[@id='table_result']//tbody//tr[@role='row']")

    root_tab_url = driver.current_url
    results = []
    for selected_row_num in range(len(best_selection_row)):
        # selected_row = driver.find_element(
        # By.XPATH, f"(//table[@id='table_result']//tbody//tr[@role='row'])[{selected_row_num+1}]")
        to_click_on_row = verify_to_click_on_row(driver, a, selected_row_num)
        # print('to click on row', to_click_on_row)
        if to_click_on_row:
            try:
                (driver, a) = duplicate_in_new_tab(driver, a, root_tab_url)
                (driver, a) = filter_all_columns(driver, a, address)
                (driver, a) = click_on_selected_row(
                    driver, a, selected_row_num)
                (driver, a) = attempt_to_update_address_information(driver, a)
                results = get_coverage_result(driver, a)
                (driver, a) = close_duplicated_tab(driver, a)

                selected_table_row_instance = SelectedTableRow.get_instance()

                selected_table_row_instance.set_result_remark(
                    self=selected_table_row_instance, result_remark=results[1])

            except NoSuchElementException:
                (driver, a) = restart_filter_process(
                    driver, a, selected_row_num, address)
                results = get_coverage_result(driver, a)
                (driver, a) = close_duplicated_tab(driver, a)

    return (driver, a)
