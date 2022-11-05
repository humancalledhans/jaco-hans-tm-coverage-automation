from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


def wait_to_decide_xpath(driver, a):
    try:
        WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
            (By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']")))

        x_code_path = "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"

    except TimeoutException:
        x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"

    return x_code_path
