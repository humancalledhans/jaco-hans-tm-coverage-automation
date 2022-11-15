from selenium.webdriver.common.by import By

import time
from src.tm_global.operations.get_coverage_result import get_coverage_result

from selenium.webdriver.common.by import By

from src.tm_global.operations.filter_all_columns import filter_all_columns
from src.tm_global.operations.click_on_selected_row import click_on_selected_row
from src.tm_global.operations.close_duplicated_tab import close_duplicated_tab

from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def restart_filter_process(driver, a, selected_row_num, address):
    while len(driver.find_elements(By.XPATH, "(//table[@id='table_result']//tbody//tr[@role='row'])")) == 0:
        driver.refresh()
        (driver, a) = pause_until_loaded(driver, a)
        (driver, a) = filter_all_columns(driver, a, address)

    (driver, a) = click_on_selected_row(
        driver, a, selected_row_num)
    return (driver, a)
