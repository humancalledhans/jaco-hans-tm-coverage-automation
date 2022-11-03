from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def enter_username_and_password(driver, a, username, password):
    user_name_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='text' and @class='form-control form-control-df']")))
    user_name_field.clear()
    user_name_field.send_keys(username)

    password_field = driver.find_element(
        By.XPATH, "//input[@type='password' and @class='form-control form-control-df']")
    password_field.clear()
    password_field.send_keys(password)

    return (driver, a)
