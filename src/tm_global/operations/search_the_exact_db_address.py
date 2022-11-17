import time
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.operations.select_state import select_state
from src.tm_global.operations.enter_into_keyword_field import enter_into_keyword_field
from src.tm_global.operations.click_on_search_btn import click_on_search_button
from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.get_num_of_results import get_num_of_results
from src.tm_global.singleton.selected_table_row import SelectedTableRow
from src.tm_global.operations.verified_that_all_the_results_are_same import verified_that_all_the_results_are_same


def try_to_search_the_full_address(driver, a):

    current_db_row_instance = CurrentDBRow.get_instance()
    address_string = current_db_row_instance.get_partial_address_without_keys(
        self=current_db_row_instance)

    # enter address into keyword field

    if address_string != '':

        (driver, a) = enter_into_keyword_field(driver, a, address_string)

        (driver, a) = click_on_search_button(driver, a)

        (driver, a) = pause_until_loaded(driver, a)

        num_of_results = get_num_of_results(driver, a)

        if num_of_results > 0 and verified_that_all_the_results_are_same(driver, a):
            selected_table_row_instance = SelectedTableRow.get_instance()
            selected_table_row_instance.set_part_of_address_used(
                self=selected_table_row_instance, part_of_address_used='Lot Num & Street Name')
            return (driver, a, True)

        else:
            driver.get(
                "https://wholesalepremium.tm.com.my/coverage-search/address")
            (driver, a) = pause_until_loaded(driver, a)
            (driver, a) = select_state(driver, a)
            return (driver, a, False)

    else:
        return (driver, a, False)
