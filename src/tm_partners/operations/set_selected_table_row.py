import time
from src.tm_partners.singleton.selected_table_row import SelectedTableRow
from selenium.webdriver.common.by import By


def set_selected_table_row(driver, a, x_code_path, selected_table_row):

    table_row_data_list = driver.find_elements(
        By.XPATH, f"({x_code_path})[{selected_table_row+1}]//td[@class='datagrid']")

    table_row_data = []
    for table_data in table_row_data_list:
        table_row_data.append(table_data.text)

    table_header_data = []
    datagrid_header = driver.find_elements(
        By.XPATH, "//tr[@class='datagrid-header']//th[@class='datagrid']")
    for tab in datagrid_header:
        if tab.text != '':
            table_header_data.append(tab.text)

    table_unit_num_index = table_header_data.index('House/Unit/Lot No.')
    table_street_type_index = table_header_data.index('Street Type')
    table_street_name_index = table_header_data.index('Street Name')
    table_section_index = table_header_data.index('Section')
    table_floor_no_index = table_header_data.index('Floor No.')
    table_building_name_index = table_header_data.index('Building Name')
    table_city_index = table_header_data.index('City')
    table_state_index = table_header_data.index('State')
    table_postcode_index = table_header_data.index('Postcode')

    table_unit_num = table_row_data[table_unit_num_index]
    table_street_type = table_row_data[table_street_type_index]
    table_street_name = table_row_data[table_street_name_index]
    table_section = table_row_data[table_section_index]
    table_floor_no = table_row_data[table_floor_no_index]
    table_building_name = table_row_data[table_building_name_index]
    table_city = table_row_data[table_city_index]
    table_state = table_row_data[table_state_index]
    table_postcode = table_row_data[table_postcode_index]

    if len(table_postcode) > 0:
        while table_postcode[0] == '0':
            table_postcode = table_postcode[1:]

    selected_table_row = SelectedTableRow.get_instance()
    selected_table_row.set_unit_no(selected_table_row, table_unit_num)
    selected_table_row.set_street_type(selected_table_row, table_street_type)
    selected_table_row.set_street_name(selected_table_row, table_street_name)
    selected_table_row.set_section(selected_table_row, table_section)
    selected_table_row.set_floor(selected_table_row, table_floor_no)
    selected_table_row.set_building(selected_table_row, table_building_name)
    selected_table_row.set_city(selected_table_row, table_city)
    selected_table_row.set_state(selected_table_row, table_state)
    selected_table_row.set_postcode(selected_table_row, table_postcode)
