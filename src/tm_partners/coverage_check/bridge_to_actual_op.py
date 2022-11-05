from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException

from src.tm_partners.operations.detect_and_solve_captcha import detect_and_solve_captcha

from src.tm_partners.singleton.current_db_row import CurrentDBRow


def bridge_to_actual_op(driver, a):
    address_string = ''
    current_db_row = CurrentDBRow.get_instance()
    input_house_unit_lotno = current_db_row.get_house_unit_lotno(
        self=current_db_row)
    input_street = current_db_row.get_street(self=current_db_row)
    input_section = current_db_row.get_section(self=current_db_row)
    input_floor_no = current_db_row.get_floor(self=current_db_row)
    input_building_name = current_db_row.get_building(
        self=current_db_row)
    input_city = current_db_row.get_city(self=current_db_row)
    input_state = current_db_row.get_state(self=current_db_row)
    input_postcode = current_db_row.get_postcode(self=current_db_row)

    if input_house_unit_lotno is None:
        input_house_unit_lotno = ''
    if input_street is None:
        input_street = ''
    if input_section is None:
        input_section = ''
    if input_floor_no is None:
        input_floor_no = ''
    if input_building_name is None:
        input_building_name = ''
    if input_city is None:
        input_city = ''
    if input_state is None:
        input_state = ''
    if input_postcode is None:
        input_postcode = ''

    address_string = address_string + \
        "House/Unit/Lot No." + input_house_unit_lotno + '\n' + \
        "Street: " + input_street + '\n' + \
        "Section: " + input_section + '\n' + \
        "Floor No: " + input_floor_no + '\n' + \
        "Building Name: " + input_building_name + '\n' + \
        "City: " + input_city + '\n' + \
        "State: " + input_state + '\n' + \
        "Postcode: " + input_postcode

    try:
        next_button = driver.find_element(
            By.XPATH, "//input[@type='image' and contains(@src, 'btnNext')]")
        a.move_to_element(next_button).click().perform()
        (driver, a) = detect_and_solve_captcha(driver, a)

        return (driver, a)

    except NoSuchElementException:
        # it means we're not at the "Type in more details" page.
        return (driver, a)
