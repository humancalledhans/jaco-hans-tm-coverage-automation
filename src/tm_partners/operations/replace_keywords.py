from selenium.webdriver.common.by import By

from src.tm_partners.operations.click_search_btn import click_search_btn
from src.tm_partners.operations.detect_and_solve_captcha import detect_and_solve_captcha
from src.tm_partners.operations.try_diff_xpath_for_results_table import try_diff_xpath_for_results_table


def replace_keywords(driver, a, keyword_search_string):
    replace_bool = False
    if "KONDOMINIUM" in keyword_search_string.upper():
        keyword_search_string = keyword_search_string.replace(
            "KONDOMINIUM", "CONDOMINIUM")
        replace_bool = True
    elif "KONDO" in keyword_search_string.upper():
        keyword_search_string = keyword_search_string.replace(
            "KONDO", "CONDO")
        replace_bool = True
    elif "JLN" in keyword_search_string.upper():
        keyword_search_string = keyword_search_string.replace(
            "JLN", "JALAN")
    if replace_bool:
        keyword_field = driver.find_element(
            By.XPATH, "//form[@name='Netui_Form_3']//input[@type='text' and contains(@name, 'searchString')]")

        keyword_field.clear()
        keyword_field.send_keys(
            keyword_search_string)

    (driver1, a1) = click_search_btn(driver, a)
    (driver2, a2) = detect_and_solve_captcha(driver1, a1)

    return try_diff_xpath_for_results_table(driver2, a2)
