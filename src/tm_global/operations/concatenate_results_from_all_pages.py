import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def concatenate_results_from_all_pages(driver, a):

    all_results = []
    table_data = driver.find_elements(
        By.XPATH, "//div[@class='dataTables_scrollBody']//table//tr[@role='row' and @class='odd']")
    for idx in range(len(table_data)):
        row_data = []
        current_row_data = driver.find_elements(
            By.XPATH, f"(//div[@class='dataTables_scrollBody']//table//tr[@role='row' and @class='odd'])[{idx}+1]//td")
        for data_idx in range(len(current_row_data)-1):
            row_data.append(current_row_data[data_idx].text)
        # note that the index is already incremented by 1.
        all_results.append((row_data, idx+1))

    num_of_results = driver.find_element(
        By.XPATH, "//p[@id='address-count']//strong").text
    if num_of_results == '':
        num_of_results = 0

    if int(num_of_results) > len(table_data):
        while len(all_results) < int(num_of_results):
            try:
                next_page_btn = driver.find_element(
                    By.XPATH, "//a[@class='paginate_button next']")
                a.move_to_element(next_page_btn).click().perform()
                (driver, a) = pause_until_loaded(driver, a)

                table_data = driver.find_elements(
                    By.XPATH, "//div[@class='dataTables_scrollBody']//table//tr[@role='row' and @class='odd']")
                # this gives us the rows. to get each data, we need to get the //td of each table_data.
                for idx in range(len(table_data)):
                    row_data = []
                    current_row_data = driver.find_elements(
                        By.XPATH, f"(//div[@class='dataTables_scrollBody']//table//tr[@role='row' and @class='odd'])[{idx}+1]//td")
                    for data_idx in range(len(current_row_data)-1):
                        row_data.append(current_row_data[data_idx].text)
                    all_results.append((row_data,))

            except NoSuchElementException:
                break
    return all_results
