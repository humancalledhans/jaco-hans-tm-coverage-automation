import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.singleton.selected_table_row import SelectedTableRow


def enter_into_section_name_filter(driver, a):
    """
    if there are no results after we filter, we take away the filter.
    """
    current_db_row = CurrentDBRow.get_instance()
    section_name = current_db_row.get_section(self=current_db_row)

    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located(
            (By.XPATH, "//td[@style='padding: 1px !important; border-color: transparent !important']//input[@type='text' and @id='section']")))
        section_name_filter_field = driver.find_element(
            By.XPATH, "//td[@style='padding: 1px !important; border-color: transparent !important']//input[@type='text' and @id='section']")
        section_name_filter_field.clear()
        section_name_filter_field.send_keys(section_name)
        (driver, a) = pause_until_loaded(driver, a)
        try:
            driver.find_element(
                By.XPATH, "//td[@class='dataTables_empty' and contains(text(), 'No matching records found')]")
            section_name_filter_field.clear()
            (driver, a) = pause_until_loaded(driver, a)
            selected_table_row_instance = SelectedTableRow.get_instance()
            selected_table_row_instance.set_used_section_name_as_filter(
                self=selected_table_row_instance, used_section_name_as_filter=False)

        except NoSuchElementException:
            selected_table_row_instance = SelectedTableRow.get_instance()
            selected_table_row_instance.set_used_section_name_as_filter(
                self=selected_table_row_instance, used_section_name_as_filter=True)

        finally:
            return (driver, a)
    except TimeoutException:
        raise Exception('Section name filter field did not pop up.')
