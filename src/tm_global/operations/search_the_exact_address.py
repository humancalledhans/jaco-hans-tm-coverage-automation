import time
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.operations.select_state import select_state
from src.tm_global.operations.enter_into_keyword_field import enter_into_keyword_field
from src.tm_global.operations.click_on_search_btn import click_on_search_button


def search_the_exact_address(driver, a, address_string):
    driver.get("https://wholesalepremium.tm.com.my/coverage-search/address")
    (driver, a) = pause_until_loaded(driver, a)

    # select state
    (driver, a) = select_state(driver, a)

    # enter address into keyword field
    (driver, a) = enter_into_keyword_field(driver, a, address_string)

    (driver, a) = click_on_search_button(driver, a)

    return (driver, a)
