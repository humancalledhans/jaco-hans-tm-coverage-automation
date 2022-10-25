from selenium.webdriver.common.by import By

def try_diff_xpath_for_results_table(driver, a):
    number_of_results = len(driver.find_elements(
        By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"))

    if number_of_results == 0:
        number_of_results = len(driver.find_elements(
            By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"))

    return (driver, a, number_of_results)
