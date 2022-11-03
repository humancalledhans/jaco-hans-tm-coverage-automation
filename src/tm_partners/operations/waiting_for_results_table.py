from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def waiting_for_results_table(driver, a):
    WebDriverWait(driver, 2).until(EC.presence_of_element_located(
        (By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")))
    return (driver, a)
