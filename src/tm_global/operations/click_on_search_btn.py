from selenium.webdriver.common.by import By

from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def click_on_search_button(driver, a):
    search_button = driver.find_element(
        By.XPATH, "//button[@type='submit' and @name='keywordSearch']")
    a.move_to_element(search_button).click().perform()

    (driver1, a1) = pause_until_loaded(driver, a)

    return (driver1, a1)
