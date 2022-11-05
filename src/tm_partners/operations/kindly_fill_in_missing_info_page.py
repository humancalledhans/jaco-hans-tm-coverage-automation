from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def kindly_fill_in_missing_info_page(driver, a):
    # for when there is the "kindly fill in the missing information" page.
    WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@id='incompleteAddress']")))
    for missing_information in driver.find_elements(By.XPATH, "//input[@type='text']"):
        missing_information.send_keys("-")
    return (driver, a)
