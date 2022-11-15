import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def verified_that_all_the_results_are_same(driver, a):
    table_data = driver.find_elements(
        By.XPATH, "//div[@class='dataTables_scrollBody']//table//tr[@role='row' and @class='odd']")
    first_row_data = []
    for idx in range(len(table_data)):
        current_row_data = driver.find_elements(
            By.XPATH, f"(//div[@class='dataTables_scrollBody']//table//tr[@role='row' and @class='odd'])[{idx}+1]//td")
        if len(first_row_data) == 0:
            for data_idx in range(len(current_row_data)-1):
                first_row_data.append(current_row_data[data_idx].text)
        else:
            for data_idx in range(len(current_row_data)-1):
                if first_row_data[data_idx] != current_row_data[data_idx].text:
                    return False

    return True
