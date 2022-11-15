import time
from selenium.webdriver.common.by import By
from src.tm_global.singleton.lot_num_match_bool import LotNumMatchBool
from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.singleton.selected_table_row import SelectedTableRow
from src.tm_global.operations.compare_all_column_data import compare_all_column_data


def verify_to_click_on_row(driver, a, selected_row_num):

    lot_num_match_bool_singleton = LotNumMatchBool.get_instance()
    lot_num_match_bool = lot_num_match_bool_singleton.get_lotnummatch(
        self=lot_num_match_bool_singleton)

    current_db_row_singleton = CurrentDBRow.get_instance()

    all_columns_match_bool = compare_all_column_data(
        driver, a, selected_row_num)

    if not lot_num_match_bool and current_db_row_singleton.get_search_level_flag(self=current_db_row_singleton):
        return False

    elif not all_columns_match_bool:
        return False

    else:
        return True
