from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def wait_for_results_table(driver, a):
    WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
        (By.XPATH, "//table[@id='resultAddressGrid']")))
    return (driver, a)
