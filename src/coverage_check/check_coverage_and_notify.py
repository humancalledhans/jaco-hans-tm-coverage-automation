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

from singleton.current_input_row_singleton import CurrentInputRow

from notifications.telegram_msg import send_message
from notifications.email_msg import send_email
from .go_back_to_search_page import go_back_to_coverage_search_page


def check_coverage_and_notify(table_row_num, driver, a):

	def check_coverage_and_notify_actual(driver, a, address_string):
		try:
			while driver.execute_script("return document.readyState;") != "complete":
				time.sleep(0.5)
			WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[4]/center/div[2]/div[2]/div/table/tbody/tr[2]/td/div[2]/div/form/div[3]/div[1]/table/tbody/tr[2]/td[1]/img[contains(@src, 'tick_checkcoverage')]")))
			# coverage available.
			send_message(address_string + "\nhas coverage!")
			send_email(address_string + "\nhas coverage!")
			### TODO: call telegram and email functions - and send notifications.
			go_back_to_coverage_search_page(driver)

		except TimeoutException:
			send_message(address_string + " does not have coverage.")
			send_email(address_string + " does not have coverage.")
			go_back_to_coverage_search_page(driver)

	def bridge_to_actual_op(driver,a):
		address_string = ''
		current_input_row_singleton = CurrentInputRow.get_instance()
		input_header_data = current_input_row_singleton.get_input_header_data(self=current_input_row_singleton)
		input_row_data = current_input_row_singleton.get_input_row_data(self=current_input_row_singleton)

		input_house_unit_lotno_index = input_header_data.index('House/Unit/Lot No.')
		input_street_type_index = input_header_data.index('Street Type')
		input_street_name_index = input_header_data.index('Street Name')
		input_section_index = input_header_data.index('Section')
		input_floor_no_index = input_header_data.index('Floor No.')
		input_building_name_index = input_header_data.index('Building Name')
		input_city_index = input_header_data.index('City')
		input_state_index = input_header_data.index('State')
		input_postcode_index = input_header_data.index('Postcode')

		input_house_unit_lotno = input_row_data[input_house_unit_lotno_index]
		input_street_type = input_row_data[input_street_type_index]
		input_street_name = input_row_data[input_street_name_index]
		input_section = input_row_data[input_section_index]
		input_floor_no = input_row_data[input_floor_no_index]
		input_building_name = input_row_data[input_building_name_index]
		input_city = input_row_data[input_city_index]
		input_state = input_row_data[input_state_index]
		input_postcode = input_row_data[input_postcode_index]

		address_string = address_string + \
			"House/Unit/Lot No." + input_house_unit_lotno + '\n' + \
			"Street Type: " + input_street_type + '\n' + \
			"Street Name: " + input_street_name + '\n' + \
			"Section: " + input_section + '\n' + \
			"Floor No: " + input_floor_no + '\n' + \
			"Building Name: " + input_building_name + '\n' + \
			"City: " + input_city + '\n' + \
			"State: " + input_state + '\n' + \
			"Postcode: " + input_postcode

		try:
			next_button = driver.find_element(By.XPATH, "//input[@type='image' and contains(@src, 'btnNext')]")
			a.move_to_element(next_button).click().perform()
			check_coverage_and_notify_actual(driver,a,address_string)
		except NoSuchElementException:
			# it means we're not at the "Type in more details" page.
			check_coverage_and_notify_actual(driver,a,address_string)


	select_button = driver.find_element(By.XPATH, f"//*[@id='resultAddressGrid']/tbody/tr[{3+table_row_num}]/td[10]/a/img")

	a.move_to_element(select_button).click().perform()
	try:
		while driver.execute_script("return document.readyState;") != "complete":
			time.sleep(0.5)

		# for when there is the "kindly fill in the missing information" page.
		WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[@id='incompleteAddress']")))
		for missing_information in driver.find_elements(By.XPATH, "//input[@type='text']"):
			missing_information.send_keys("-")

		bridge_to_actual_op(driver,a)


	except TimeoutException:
		# for when there is NOT the "kindly fill in the missing information" page.
		while driver.execute_script("return document.readyState;") != "complete":
			time.sleep(0.5)

		try:
			WebDriverWait(driver,150).until(EC.presence_of_element_located((By.XPATH, "//table[@align='center' and @class='Yellow']")))
			bridge_to_actual_op(driver, a)

		except TimeoutException:
			driver.refresh()
			try:
				WebDriverWait(driver,150).until(EC.presence_of_element_located((By.XPATH, "//table[@align='center' and @class='Yellow']")))
				bridge_to_actual_op(driver, a)
			
			except TimeoutException:
				raise Exception("Check failed. Code has refreshed and waited for 5 minutes - but the Coverage result never showed.")
				driver.execute_script("window.history.go(-1)")