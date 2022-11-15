import time
from selenium.webdriver.common.by import By
from src.tm_global.singleton.lot_num_match_bool import LotNumMatchBool
from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.singleton.selected_table_row import SelectedTableRow


def compare_all_column_data(driver, a, selected_row_num):
    selected_row_unit_num = driver.find_element(
        By.XPATH, f"((//table[@id='table_result']//tbody//tr[@role='row'])[{selected_row_num+1}]//td)[1]").text

    selected_row_street_type = driver.find_element(
        By.XPATH, f"((//table[@id='table_result']//tbody//tr[@role='row'])[{selected_row_num+1}]//td)[2]").text

    selected_row_street_name = driver.find_element(
        By.XPATH, f"((//table[@id='table_result']//tbody//tr[@role='row'])[{selected_row_num+1}]//td)[3]").text

    selected_row_section = driver.find_element(
        By.XPATH, f"((//table[@id='table_result']//tbody//tr[@role='row'])[{selected_row_num+1}]//td)[4]").text

    selected_row_floor_no = driver.find_element(
        By.XPATH, f"((//table[@id='table_result']//tbody//tr[@role='row'])[{selected_row_num+1}]//td)[5]").text

    selected_row_building_name = driver.find_element(
        By.XPATH, f"((//table[@id='table_result']//tbody//tr[@role='row'])[{selected_row_num+1}]//td)[6]").text

    selected_row_city = driver.find_element(
        By.XPATH, f"((//table[@id='table_result']//tbody//tr[@role='row'])[{selected_row_num+1}]//td)[7]").text

    selected_row_postcode = driver.find_element(
        By.XPATH, f"((//table[@id='table_result']//tbody//tr[@role='row'])[{selected_row_num+1}]//td)[8]").text

    selected_table_row_singleton = SelectedTableRow.get_instance()
    selected_table_row_unit_no = selected_table_row_singleton.get_unit_no(
        self=selected_table_row_singleton)
    selected_table_row_street_type = selected_table_row_singleton.get_street_type(
        self=selected_table_row_singleton)
    selected_table_row_street_name = selected_table_row_singleton.get_street_name(
        self=selected_table_row_singleton)
    selected_table_row_section = selected_table_row_singleton.get_section(
        self=selected_table_row_singleton)
    selected_table_row_floor_no = selected_table_row_singleton.get_floor(
        self=selected_table_row_singleton)
    selected_table_row_building_name = selected_table_row_singleton.get_building(
        self=selected_table_row_singleton)
    selected_table_row_city = selected_table_row_singleton.get_city(
        self=selected_table_row_singleton)
    selected_table_row_postcode = selected_table_row_singleton.get_postcode(
        self=selected_table_row_singleton)

    # print('selected_row_unit_num', selected_row_unit_num)
    # print('selected_row_street_type', selected_row_street_type)
    # print('selected_row_street_name', selected_row_street_name)
    # print('selected_row_section', selected_row_section)
    # print('selected_row_floor_no', selected_row_floor_no)
    # print('selected_row_building_name', selected_row_building_name)
    # print('selected_row_city', selected_row_city)
    # print('selected_row_postcode', selected_row_postcode)

    # print('selected_table_row_unit_no', selected_table_row_unit_no)
    # print('selected_table_row_street_type', selected_table_row_street_type)
    # print('selected_table_row_street_name', selected_table_row_street_name)
    # print('selected_table_row_section', selected_table_row_section)
    # print('selected_table_row_floor_no', selected_table_row_floor_no)
    # print('selected_table_row_building_name', selected_table_row_building_name)
    # print('selected_table_row_city', selected_table_row_city)
    # print('selected_table_row_postcode', selected_table_row_postcode)

    if selected_row_unit_num == selected_table_row_unit_no and \
            selected_row_street_type == selected_table_row_street_type and \
            selected_row_street_name == selected_table_row_street_name and \
            selected_row_section == selected_table_row_section and \
            selected_row_floor_no == selected_table_row_floor_no and \
            selected_row_building_name == selected_table_row_building_name and \
            selected_row_city == selected_table_row_city and \
            selected_row_postcode == selected_table_row_postcode:
        return True

    else:
        return False
