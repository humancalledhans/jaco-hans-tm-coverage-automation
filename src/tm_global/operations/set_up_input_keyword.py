import time
from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.enter_into_keyword_field import enter_into_keyword_field
from src.tm_global.operations.click_on_search_btn import click_on_search_button
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from selenium.webdriver.common.by import By

from src.tm_global.operations.get_num_of_results import get_num_of_results
from src.tm_global.operations.return_to_coverage_search_page import (
    return_to_coverage_search_page,
)
from src.tm_global.operations.reset_for_next_search import reset_for_next_search
from src.tm_global.singleton.selected_table_row import SelectedTableRow

keyword_search_string = ""


def try_using_building_name(driver, a):

    current_db_row = CurrentDBRow.get_instance()

    building_name = current_db_row.get_building(self=current_db_row)

    if building_name is not None:
        building_name = building_name.strip()

    if building_name != "" and building_name is not None and len(building_name) > 3:
        global keyword_search_string
        keyword_search_string = keyword_search_string + " " + building_name

        (driver, a) = enter_into_keyword_field(driver, a, keyword_search_string)

        (driver, a) = click_on_search_button(driver, a)

        (driver, a) = pause_until_loaded(driver, a)

        num_of_results = get_num_of_results(driver, a)

        return (driver, a, num_of_results)

    else:
        return (driver, a, 0)


def try_using_street(driver, a):

    current_db_row = CurrentDBRow.get_instance()

    street = current_db_row.get_street(self=current_db_row)

    if street is not None:
        street = street.strip()

    if street != "" and street is not None and len(street) > 3:
        # append a space + the street name to the keyword search string
        global keyword_search_string
        keyword_search_string = keyword_search_string + " " + street

        (driver, a) = enter_into_keyword_field(driver, a, keyword_search_string)

        (driver, a) = click_on_search_button(driver, a)

        (driver, a) = pause_until_loaded(driver, a)

        num_of_results = get_num_of_results(driver, a)

        return (driver, a, num_of_results)

    else:
        return (driver, a, 0)


def try_using_section(driver, a):
    current_db_row = CurrentDBRow.get_instance()

    section = current_db_row.get_section(self=current_db_row)

    if section is not None:
        section = section.strip()

    if section != "" and section is not None and len(section) > 3:
        global keyword_search_string
        keyword_search_string = section

        (driver, a) = enter_into_keyword_field(driver, a, keyword_search_string)

        (driver, a) = click_on_search_button(driver, a)

        (driver, a) = pause_until_loaded(driver, a)

        num_of_results = get_num_of_results(driver, a)

        return (driver, a, num_of_results)

    else:
        return (driver, a, 0)


def enter_right_keyword(driver, a):

    # step 1: check if there is a building name.
    keyword_search_string = ""
    (driver, a, num_of_results_from_section) = try_using_section(driver, a)
    if num_of_results_from_section > 0:
        return result_using_street(driver, a)
    current_db_row = CurrentDBRow.get_instance()
    print(current_db_row.get_id(self=current_db_row))
    print()
    return "No results found using building name, street name, or section name."


# TODO Rename this here and in `enter_right_keyword`
def result_using_street(driver, a):
    # independent copy of driver and a
    (section_driver, section_a) = (driver, a)
    # step 2: no results using building name. check if there is a street name.
    (driver, a) = reset_for_next_search(driver, a)
    (driver, a, num_of_results_from_street_name) = try_using_street(driver, a)

    # return (driver, a)

    # # step 2: no results using section name. check if there is a street name.
    # (driver, a) = reset_for_next_search(driver, a)
    # (driver, a, num_of_results_from_street_name) = try_using_street(driver, a)

    if num_of_results_from_street_name > 0:
        return result_using_building(driver, a)
    (driver, a) = reset_for_next_search(driver, a)
    (driver, a, num_of_results_from_section) = try_using_section(driver, a)

    return set_results("Section Name", section_driver, section_a)


# TODO Rename this here and in `enter_right_keyword`
def result_using_building(driver, a):
    # independent copy of driver and a
    (street_driver, street_a) = (driver, a)
    # step 3: no results using building name and street name. try using section name.
    (driver, a) = reset_for_next_search(driver, a)
    (
        driver,
        a,
        num_of_results_from_building_name,
    ) = try_using_building_name(driver, a)

    if num_of_results_from_building_name > 0:
        return set_results("Building Name", driver, a)
    (driver, a) = reset_for_next_search(driver, a)
    (
        driver,
        a,
        num_of_results_from_street_name,
    ) = try_using_street(driver, a)
    return set_results("Street Name", street_driver, street_a)


# TODO Rename this here and in `enter_right_keyword`
def set_results(part_of_address_used, driver, a):
    # print('building name results: ' +
    #   str(num_of_results_from_building_name))
    selected_table_row_instance = SelectedTableRow.get_instance()
    selected_table_row_instance.set_part_of_address_used(
        self=selected_table_row_instance, part_of_address_used=part_of_address_used
    )

    return (driver, a)
