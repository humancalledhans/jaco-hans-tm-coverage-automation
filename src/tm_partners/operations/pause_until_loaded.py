import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait



def pause_until_loaded(driver, a):
    while driver.execute_script("return document.readyState;") != "complete":
        time.sleep(0.5)

    return (driver, a)
