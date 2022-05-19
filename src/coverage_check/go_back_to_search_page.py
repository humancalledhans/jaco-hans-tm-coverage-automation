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

def go_back_to_coverage_search_page(driver):
	driver.execute_script("window.history.go(-1)")
	while driver.execute_script("return document.readyState;") != "complete":
		time.sleep(0.5)

	try:
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//select[@id='actionForm_state']")))
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//select[@id='actionForm_state']")))
		return

	except TimeoutException:
		go_back_to_coverage_search_page(driver)