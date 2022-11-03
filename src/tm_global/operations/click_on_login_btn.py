from selenium.webdriver.common.by import By

from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def click_on_login_button(driver, a):
    login_button = driver.find_element(
        By.XPATH, "//button[@type='submit' and @class='btn btn-orange-white w-100']")
    a.move_to_element(login_button).click().perform()

    (driver1, a1) = pause_until_loaded(driver, a)

    return (driver1,a1)
