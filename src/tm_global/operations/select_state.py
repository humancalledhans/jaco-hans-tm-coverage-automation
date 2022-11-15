from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.assumptions.accepted_states_list import get_accepted_states

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def select_state(driver, a):
    current_db_row = CurrentDBRow.get_instance()
    accepted_states_list = get_accepted_states()
    current_row_id = current_db_row.get_id(self=current_db_row)
    state = current_db_row.get_state(self=current_db_row)

    if state in accepted_states_list:
        state_tab = Select(driver.find_element(
            By.XPATH, "//select[@name='STATE' and @id='dropdownState']"))
        state_tab.select_by_visible_text(f"{state}")
    elif state == 'LABUAN':
        state_tab = Select(driver.find_element(
            By.XPATH, "//select[@name='STATE' and @id='dropdownState']"))
        state_tab.select_by_visible_text("WILAYAH PERSEKUTUAN LABUAN")
    elif state == 'PUTRAJAYA':
        state_tab = Select(driver.find_element(
            By.XPATH, "//select[@name='STATE' and @id='dropdownState']"))
        state_tab.select_by_visible_text("WILAYAH PERSEKUTUAN PUTRAJAYA")

    else:
        raise Exception(f"\n*****\n\nERROR IN id {current_row_id} OF DATABASE - \n\n*****\n\
The State in ROW {current_row_id} is {state}. \n\
State needs to be one of \'MELAKA\', \'KELANTAN\', \'KEDAH\', \'JOHOR\', \
\'NEGERI SEMBILAN\', \'PAHANG\', \'PERAK\', \'PERLIS\', \
\'PULAU PINANG\', \'SABAH\', \'SARAWAK\', \'SELANGOR\', \'TERENGGANU\', \
\'LABUAN\', \'PUTRAJAYA\', \
\'WILAYAH PERSEKUTUAN\', \'WILAYAH PERSEKUTUAN LABUAN\', \
\'WILAYAH PERSEKUTUAN PUTRAJAYA\'\n*****\n")

    return (driver, a)
