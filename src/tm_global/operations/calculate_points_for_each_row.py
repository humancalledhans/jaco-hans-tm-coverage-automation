import time
from selenium.webdriver.common.by import By

from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.assumptions.table_column_headers_assumption import return_assummed_table_column_headers


def calculate_points_for_each_row(driver, a, result):
    """
    returns a tuple. (points, lotNumAndStreetAndPostcodeNoMatchBool)
    """
    # table_column_headers = []
    # table_column_headers_from_site = driver.find_elements(
    #     By.XPATH, "//div[@class='dataTables_scrollHead']//tr[@role='row'][1]//th[@class='sorting_disabled' and @rowspan='1']")
    # for header in table_column_headers_from_site:
    #     if header.text != '':
    #         table_column_headers.append(header.text)

    # print("table column headers", table_column_headers)
    table_column_headers = return_assummed_table_column_headers()


    table_column_data = []
    if len(result) == 2:
        for res in result[0]:
            table_column_data.append(res)
    elif len(result) == 1:
        for res in result[0]:
            table_column_data.append(res)

    table_house_unit_no = table_column_data[table_column_headers.index(
        'House / Unit No')]
    table_street_type = table_column_data[table_column_headers.index(
        'Street Type')]
    table_street_name = table_column_data[table_column_headers.index(
        'Street Name')]
    table_street = table_street_type + ' ' + table_street_name
    table_section = table_column_data[table_column_headers.index('Section')]
    table_floor_no = table_column_data[table_column_headers.index('Floor No')]
    table_building_name = table_column_data[table_column_headers.index(
        'Building Name')]
    table_city = table_column_data[table_column_headers.index('City')]
    table_postcode = table_column_data[table_column_headers.index('Postcode')]
    table_cable_type = table_column_data[table_column_headers.index(
        'Cable Type')]
    # table_address_type = table_column_data[table_column_headers.index(
    # 'Address Type')]

    current_db_row = CurrentDBRow.get_instance()
    current_row_unit_no = current_db_row.get_house_unit_lotno(
        self=current_db_row)
    current_row_street = current_db_row.get_street(self=current_db_row)
    current_row_section = current_db_row.get_section(self=current_db_row)
    current_row_floor_no = current_db_row.get_floor(
        self=current_db_row)
    current_row_building_name = current_db_row.get_building(
        self=current_db_row)
    current_row_city = current_db_row.get_city(self=current_db_row)
    current_row_postcode = current_db_row.get_postcode(
        self=current_db_row)
    current_row_unit_num_match_bool = current_db_row.get_search_level_flag(
        self=current_db_row)

    # print("\n/ / / / / / / / / / / / / / / / / / / / / \n")
    # print("current_row", "table_house")
    # print("current_row_unit_num_match_bool", current_row_unit_num_match_bool)
    # print("lot no.", current_row_unit_no, table_house_unit_no)
    # print("street", current_row_street, table_street)
    # print("section", current_row_section, table_section)
    # print("floor no.", current_row_floor_no, table_floor_no)
    # print("building name", current_row_building_name, table_building_name)
    # print("city", current_row_city, table_city)
    # print("postcode", current_row_postcode, table_postcode)
    # print("\n/ / / / / / / / / / / / / / / / / / / / / \n")

    # unit num needs to be matched when unit_num_match_bool == 1
    if current_row_unit_num_match_bool == 1 and \
        str(current_row_unit_no) != str(table_house_unit_no) and \
            ("LOT " + current_row_unit_no) != str(table_house_unit_no) and \
            ("LOT" + current_row_unit_no) != str(table_house_unit_no):
        return (0, None)

    # street name needs to be matching.
    if current_row_street.strip().upper() != table_street.strip().upper():
        return (0, None)

    if len(table_postcode) > 0:
        while table_postcode[0] == '0':
            table_postcode = table_postcode[1:]

    max_points = 0

    if table_house_unit_no is not None and table_house_unit_no != '' and table_house_unit_no != '-':
        max_points += 1
    if table_street is not None and table_street != '' and table_street != '-':
        max_points += 1
    if table_section is not None and table_section != '' and table_section != '-':
        max_points += 1
    if table_floor_no is not None and table_floor_no != '' and table_floor_no != '-':
        max_points += 1
    if table_building_name is not None and table_building_name != '' and table_building_name != '-':
        max_points += 1
    if table_city is not None and table_city != '' and table_city != '-':
        max_points += 1
    if table_postcode is not None and table_postcode != '' and table_postcode != '-':
        max_points += 1

    accumulated_points = 0

    lotNumAndStreetNumMatchBool = True

    if current_row_unit_no is not None and current_row_unit_no != '':
        if current_row_unit_no.strip() == table_house_unit_no.strip():
            accumulated_points = accumulated_points + 1
        else:
            lotNumAndStreetNumMatchBool = False
            if ',' in current_row_unit_no.strip():
                for lotNum in current_row_unit_no.strip().split(','):
                    if lotNum == table_house_unit_no.strip():
                        accumulated_points = accumulated_points + 1
                        break
            elif ' ' in current_row_unit_no.strip():
                for lotNum in current_row_unit_no.strip().split(' '):
                    if lotNum == table_house_unit_no.strip():
                        accumulated_points = accumulated_points + 1
                        break

    if current_row_street is not None and current_row_street != '':
        if current_row_street.upper().strip() == table_street.upper().strip():
            accumulated_points = accumulated_points + 2
        else:
            lotNumAndStreetNumMatchBool = False
    if current_row_section is not None and current_row_section != '':
        if current_row_section.upper().strip() == table_section.upper().strip():
            accumulated_points = accumulated_points + 2
    if current_row_floor_no is not None and current_row_floor_no != '':
        if current_row_floor_no == table_floor_no:
            accumulated_points = accumulated_points + 1
    if current_row_building_name is not None and current_row_building_name != '':
        if current_row_building_name.upper().strip() == table_building_name.upper().strip():
            accumulated_points = accumulated_points + 2
    if current_row_city is not None and current_row_city != '':
        if current_row_city.upper().strip() == table_city.upper().strip():
            accumulated_points = accumulated_points + 1
    if current_row_postcode is not None and current_row_postcode != '':
        if current_row_postcode == table_postcode:
            accumulated_points = accumulated_points + 1

    if accumulated_points == max_points:
        return ("BEST MATCH", True)

    return (accumulated_points, lotNumAndStreetNumMatchBool)
