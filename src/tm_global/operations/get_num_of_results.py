from selenium.webdriver.common.by import By


def get_num_of_results(driver, a):
    num_of_results = driver.find_element(
        By.XPATH, "//p[@id='address-count']//strong").text
    if num_of_results == '':
        num_of_results = 0
    return int(num_of_results)
