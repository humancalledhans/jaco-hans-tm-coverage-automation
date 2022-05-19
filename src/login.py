# login('DPSL9701', 'Djns513!!', driver)

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

import cv2
import os
import csv
import time

from PIL import Image
from coverage_check.coverage_check import finding_coverage
from solve_captcha import solve_captcha
from anticaptchaofficial.imagecaptcha import *

def login(username:str, password:str):

	proceed = False
	count = 0
	while not proceed:
		try:
			s = Service(ChromeDriverManager().install())    
			options = Options()
			options.headless = False
			options.add_argument('--disable-dev-shm-usage')
			driver = webdriver.Chrome(service=s, options=options)
			driver.get('https://partners.unifi.my/HSBBPartnerPortal/HSBBPartnerPortal.portal?_nfpb=true&_pageLabel=login_portal&_nfls=false#wlp_HSBBPartnerPortal_portal_HelpCustomer/')
			while driver.execute_script("return document.readyState;") != "complete":
				time.sleep(0.5)

			user_name_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @id='portal.actionForm_username']")))
			user_name_field.clear()
			user_name_field.send_keys(username)

			password_field = driver.find_element(By.XPATH, "//input[@type='password' and @id='portal.actionForm_password']")
			password_field.clear()
			password_field.send_keys(password)

			proceed = True

		except TimeoutException:
			count += 1
			print("Unable to access page. Trying again automatically in 10 seconds...")
			driver.close()
			time.sleep(15)
			print("15 seconds has passed. Trying Again...")

			if count == 5:
				print("We tried for 5 times. Skipping...")
				print("An hour has passed. Trying Again...")
				count = 0

	a = ActionChains(driver)

	to_proceed = False
	while to_proceed == False:
		captcha_to_solve = driver.find_element(By.XPATH, "//img[@border='1' and @style='width: 220px;']")
		captcha_code = solve_captcha(captcha_elem_to_solve=captcha_to_solve, driver=driver)

		captcha_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @id='portal.actionForm_captchaCode']")))
		captcha_field.clear()
		captcha_field.send_keys(captcha_code)

		login_button = driver.find_element(By.XPATH, "//input[@type='image' and @alt='Login']")
		a.move_to_element(login_button).click().perform()

		try:
			WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

		except TimeoutException:
			to_proceed = True

	finding_coverage(driver=driver, a=a)


if __name__ == '__main__':
	start_project()
