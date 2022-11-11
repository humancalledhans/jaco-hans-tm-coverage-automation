import time
from src.tm_partners.singleton.current_db_row import CurrentDBRow
from src.tm_partners.operations.enter_into_keyword_field import enter_into_keyword_field
from src.tm_partners.operations.click_search_btn import click_search_btn
from src.tm_partners.operations.pause_until_loaded import pause_until_loaded
from src.tm_partners.operations.wait_for_results_table import wait_for_results_table


def search_using_street_type_and_name(driver, a):
    current_db_row = CurrentDBRow.get_instance()

    unit_lotno = current_db_row.get_house_unit_lotno(
        self=current_db_row).strip()
    street = current_db_row.get_street(
        self=current_db_row).strip()

    keyword_search_string = ''
    if len(unit_lotno) > 0:
        keyword_search_string = keyword_search_string + unit_lotno + ' '
    keyword_search_string = keyword_search_string + \
        street

    (driver, a) = enter_into_keyword_field(
        driver, a, keyword_search_string)

    (driver, a) = click_search_btn(driver=driver, a=a)

    (driver, a) = pause_until_loaded(driver, a)
    (driver, a) = wait_for_results_table(driver, a)

    return (driver, a)
