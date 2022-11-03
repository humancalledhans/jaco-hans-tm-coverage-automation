from selenium.webdriver.common.by import By


def enter_into_keyword_field(driver, a, keyword_search_string):
    keyword_field = driver.find_element(
        By.XPATH, "//form[@name='Netui_Form_3']//input[@type='text' and contains(@name, 'searchString')]")
    keyword_field.clear()
    keyword_field.send_keys(keyword_search_string)
    return (driver, a)
