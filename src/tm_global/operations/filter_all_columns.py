from selenium.webdriver.common.by import By


def filter_all_columns(driver, a, address):
    data_for_each_column = address[0][0]

    all_column_inputs = driver.find_elements(
        By.XPATH, "//tr[@style='height: 0px !important;']//td//input[@type='text']")

    for input_idx in range(len(all_column_inputs)-1):
        all_column_inputs[input_idx].clear()
        all_column_inputs[input_idx].send_keys(data_for_each_column[input_idx])

    return (driver, a)
