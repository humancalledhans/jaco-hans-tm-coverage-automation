from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains


def input_speed_requested(driver, a):
    # inputing the "speed requested"
    speed_requested_tab = Select(driver.find_element(
        By.XPATH, "(//div[@class='partnerHomeContent'])[3]//select"))
    speed_requested_tab.select_by_visible_text("50Mbps and above")

    check_coverage_button = driver.find_element(
        By.XPATH, "//input[@type='image' and @value='Next' and @alt='submit']")
    a.move_to_element(check_coverage_button).click().perform()
