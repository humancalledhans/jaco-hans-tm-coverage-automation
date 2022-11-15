import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.assumptions.accepted_street_types_list import get_accepted_street_types
from src.tm_global.singleton.selected_table_row import SelectedTableRow


def enter_into_street_name_filter(driver, a):
    """
    if there are no results after we filter, we take away the unit number filter.
    """
    current_db_row = CurrentDBRow.get_instance()
    street_name = current_db_row.get_street(self=current_db_row)

    for street_type in get_accepted_street_types():
        if street_type in street_name:
            street_name = (street_name.replace(
                street_type, '')).strip()
            break

    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located(
            (By.XPATH, "//td[@style='padding: 1px !important; border-color: transparent !important']//input[@type='text' and @id='street_name']")))
        street_name_filter_field = driver.find_element(
            By.XPATH, "//td[@style='padding: 1px !important; border-color: transparent !important']//input[@type='text' and @id='street_name']")
        street_name_filter_field.clear()
        street_name_filter_field.send_keys(street_name)
        (driver, a) = pause_until_loaded(driver, a)
        try:
            driver.find_element(
                By.XPATH, "//td[@class='dataTables_empty' and contains(text(), 'No matching records found')]")
            street_name_filter_field.clear()
            (driver, a) = pause_until_loaded(driver, a)
            selected_table_row_instance = SelectedTableRow.get_instance()
            selected_table_row_instance.set_used_street_name_as_filter(
                self=selected_table_row_instance, used_street_name_as_filter=False)

        except NoSuchElementException:
            selected_table_row_instance = SelectedTableRow.get_instance()
            selected_table_row_instance.set_used_street_name_as_filter(
                self=selected_table_row_instance, used_street_name_as_filter=True)
        finally:
            return (driver, a)
    except TimeoutException:
        raise Exception('Street name filter field did not pop up.')
