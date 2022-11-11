import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait


def website_under_maintenance_wait(driver, a):
    WebDriverWait(driver, 0.5).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@id='main']//div[@id='block_feature']//div[@id='support-enquiry']")))
    print(
        "website under maintenance. retrying in 3 minutes...")
    time.sleep(60)
    print(
        "website under maintenance. retrying in 2 minutes...")
    time.sleep(60)
    print(
        "website under maintenance. retrying in 1 minute...")
    time.sleep(60)
    print("website under maintenance. retrying now...")

    return (driver, a)
