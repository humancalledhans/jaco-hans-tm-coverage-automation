import time
from selenium.webdriver.common.by import By
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.singleton.lot_num_match_bool import LotNumMatchBool
from src.tm_global.singleton.current_db_row import CurrentDBRow


def click_on_selected_row(driver, a, selected_row_num):
    row_to_click_on = driver.find_element(
        By.XPATH, f"(//table[@id='table_result']//tbody//tr[@role='row'])[{selected_row_num+1}]")

    a.move_to_element(
        row_to_click_on).click().perform()
    (driver, a) = pause_until_loaded(driver, a)

    return (driver, a)
