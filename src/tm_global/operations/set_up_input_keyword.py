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

# [City, Postcode, Section, Street, Building, Lot Number]
keyword_search_string_list = ["", "", "", "", "", ""]
keyword_search_string_name = [
    "City Name",
    "Postcode",
    "Section Name",
    "Street Name",
    "Building Name",
    "Lot Number",
]


def enter_right_keyword(driver, a):

    global keyword_search_string_name
    global keyword_search_string_list
    keyword_search_string_list = ["", "", "", "", "", ""]

    current_db_row = CurrentDBRow.get_instance()
    city = current_db_row.get_city(self=current_db_row)
    postcode = current_db_row.get_postcode(self=current_db_row)
    section = current_db_row.get_section(self=current_db_row)
    street = current_db_row.get_street(self=current_db_row)
    building_name = current_db_row.get_building(self=current_db_row)
    lot_number = current_db_row.get_house_unit_lotno(self=current_db_row)

    if city is not None:
        city = city.strip()
    if postcode is not None:
        postcode = postcode.strip()
    if section is not None:
        section = section.strip()
    if street is not None:
        street = street.strip()
    if building_name is not None:
        building_name = building_name.strip()
    if lot_number is not None:
        lot_number = lot_number.strip()

    keyword_search_string_list = [
        city,
        postcode,
        section,
        street,
        building_name,
        lot_number,
    ]

    flag = False
    first_non_none = 0

    for i in range(len(keyword_search_string_list)):
        if keyword_search_string_list[i] == "" or keyword_search_string_list[i] is None:
            continue

        if flag == False:
            first_non_none = i
            flag = True

        keyword_search_string = " ".join(
            [x for x in keyword_search_string_list[: i + 1] if x]
        )

        (driver, a) = enter_into_keyword_field(driver, a, keyword_search_string)
        (driver, a) = click_on_search_button(driver, a)
        (driver, a) = pause_until_loaded(driver, a)
        num_of_results = get_num_of_results(driver, a)

        if num_of_results > 0 and i == len(keyword_search_string_list) - 1:
            return set_results(keyword_search_string_name[i], driver, a)

        if num_of_results <= 0:
            if i == first_non_none:
                break
            (driver, a) = reset_for_next_search(driver, a)
            keyword_search_string = " ".join(
                [x for x in keyword_search_string_list[:i] if x]
            )

            (driver, a) = enter_into_keyword_field(driver, a, keyword_search_string)
            (driver, a) = click_on_search_button(driver, a)
            (driver, a) = pause_until_loaded(driver, a)
            num_of_results = get_num_of_results(driver, a)
            return set_results(keyword_search_string_name[i - 1], driver, a)

        (driver, a) = reset_for_next_search(driver, a)
    current_db_row = CurrentDBRow.get_instance()
    print(current_db_row.get_id(self=current_db_row))
    print()
    return "No results found."


def set_results(part_of_address_used, driver, a):
    # print('building name results: ' +
    #   str(num_of_results_from_building_name))
    selected_table_row_instance = SelectedTableRow.get_instance()
    selected_table_row_instance.set_part_of_address_used(
        self=selected_table_row_instance, part_of_address_used=part_of_address_used
    )

    return (driver, a)
