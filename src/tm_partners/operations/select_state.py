from src.tm_partners.operations.detect_and_solve_captcha import detect_and_solve_captcha
from src.tm_partners.singleton.current_db_row import CurrentDBRow

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def select_state(driver, a, state):
    # TODO: add condition for when there is only 'Wilayah Persekutuan' in the list.
    # if len(driver.find_elements(By.XPATH, "//select[@id='actionForm_state']//option")) == 1:
    # 	a.move_to_element(driver.find_element(By.XPATH, "//a[contains(text(), 'Help new customer')]")).click().perform()

    (driver, a) = detect_and_solve_captcha(driver, a)

    current_db_row = CurrentDBRow.get_instance()
    accepted_states_list = current_db_row.get_accepted_states_list(
        self=current_db_row)
    current_row_id = current_db_row.get_id(self=current_db_row)

    if state in accepted_states_list:
        state_tab = Select(driver.find_element(
            By.XPATH, "//select[@id='actionForm_state']"))
        state_tab.select_by_visible_text(f"{state}")
    elif state == 'LABUAN':
        state_tab = Select(driver.find_element(
            By.XPATH, "//select[@id='actionForm_state']"))
        state_tab.select_by_visible_text("WILAYAH PERSEKUTUAN LABUAN")
    elif state == 'PUTRAJAYA':
        state_tab = Select(driver.find_element(
            By.XPATH, "//select[@id='actionForm_state']"))
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

    (driver, a) = detect_and_solve_captcha(driver, a)

    return (driver, a)
