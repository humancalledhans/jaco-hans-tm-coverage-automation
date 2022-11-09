import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def enter_into_lot_number_filter(driver, a):
    """
    if there are no results after we filter, we take away the unit number filter.
    """
    current_db_row = CurrentDBRow.get_instance()
    lot_number = current_db_row.get_house_unit_lotno(self=current_db_row)
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located(
            (By.XPATH, "//td[@style='padding: 1px !important; border-color: transparent !important']//input[@type='text' and @id='house_unit_lot']")))
        lot_num_filter_field = driver.find_element(
            By.XPATH, "//td[@style='padding: 1px !important; border-color: transparent !important']//input[@type='text' and @id='house_unit_lot']")
        lot_num_filter_field.clear()
        lot_num_filter_field.send_keys(lot_number)
        (driver, a) = pause_until_loaded(driver, a)
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located(
                (By.XPATH, "//td[@class='dataTables_empty']")))
            lot_num_filter_field.clear()
            (driver, a) = pause_until_loaded(driver, a)

        except TimeoutError:
            None

        finally:
            return (driver, a)
    except TimeoutException:
        raise Exception('Lot number filter field did not pop up.')
