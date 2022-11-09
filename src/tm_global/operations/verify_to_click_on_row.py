import time
from selenium.webdriver.common.by import By
from src.tm_global.singleton.lot_num_match_bool import LotNumMatchBool
from src.tm_global.singleton.current_db_row import CurrentDBRow


def verify_to_click_on_row(driver, a, selected_row_num):
    selected_row_unit_num = driver.find_element(
        By.XPATH, f"((//table[@id='table_result']//tbody//tr[@role='row'])[{selected_row_num+1}]//td)[1]").text

    lot_num_match_bool_singleton = LotNumMatchBool.get_instance()
    lot_num_match_bool = lot_num_match_bool_singleton.get_lotnummatch(
        self=lot_num_match_bool_singleton)

    current_db_row_singleton = CurrentDBRow.get_instance()
    current_db_row_lotno = current_db_row_singleton.get_house_unit_lotno(
        self=current_db_row_singleton)

    if lot_num_match_bool:
        if str(selected_row_unit_num) != str(current_db_row_lotno):
            return False
        else:
            return True

    return True
