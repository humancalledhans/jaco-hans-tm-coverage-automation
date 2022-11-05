from selenium.webdriver.common.by import By
from src.tm_partners.operations.detect_and_solve_captcha import detect_and_solve_captcha

def enter_into_keyword_field(driver, a, keyword_search_string):
    keyword_field = driver.find_element(
        By.XPATH, "//input[@name='AddressKeyword' and @type='text']")
    keyword_field.clear()
    keyword_field.send_keys(keyword_search_string)
    (driver, a) = detect_and_solve_captcha(driver, a)

    return (driver, a)
