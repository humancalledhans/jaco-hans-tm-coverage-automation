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

import re
import cv2
import os
import csv
import time

from telegram_msg import send_message
from email_msg import send_email
from PIL import Image
from solve_captcha import solve_captcha
from anticaptchaofficial.imagecaptcha import *

def return_points_for_row(table_row_data_list, table_header_data, input_row_data, input_header_data, driver)->bool:
	"""
	could return "CONFIRMED MATCH" for max possible matches, or the number of columns matched.
	"""
	table_row_data = []
	for table_data in table_row_data_list:
		table_row_data.append(table_data.text)

	print("TABLE HEADER DATA: ", table_header_data)
	print("TABLE_ROW_DATA: ", table_row_data)

	print("INPUT_ROW_DATA: ", input_row_data)
	print("INPUT_HEADER_DATA: ", input_header_data)

	input_unit_num_match_bool_index = input_header_data.index('unit_num_match (Y/N)')
	input_unit_num_match_bool = input_row_data[input_unit_num_match_bool_index]

	input_house_unit_lotno_index = input_header_data.index('House/Unit/Lot No.')
	input_house_unit_lotno = input_row_data[input_house_unit_lotno_index]

	table_house_unit_lotno_index = table_header_data.index('House/Unit/Lot No.')
	table_house_unit_lotno = table_row_data[table_house_unit_lotno_index]

	if input_house_unit_lotno != table_house_unit_lotno and input_unit_num_match_bool == 'Y':
		return 0

	else:
		input_street_type_index = input_header_data.index('Street Type')
		input_street_name_index = input_header_data.index('Street Name')
		input_section_index = input_header_data.index('Section')
		input_floor_no_index = input_header_data.index('Floor No.')
		input_building_name_index = input_header_data.index('Building Name')
		input_city_index = input_header_data.index('City')
		input_state_index = input_header_data.index('State')
		input_postcode_index = input_header_data.index('Postcode')

		input_street_type = input_row_data[input_street_type_index]
		input_street_name = input_row_data[input_street_name_index]
		input_section = input_row_data[input_section_index]
		input_floor_no = input_row_data[input_floor_no_index]
		input_building_name = input_row_data[input_building_name_index]
		input_city = input_row_data[input_city_index]
		input_state = input_row_data[input_state_index]
		input_postcode = input_row_data[input_postcode_index]


		table_street_type_index = table_header_data.index('Street Type')
		table_street_name_index = table_header_data.index('Street Name')
		table_section_index = table_header_data.index('Section')
		table_floor_no_index = table_header_data.index('Floor No.')
		table_building_name_index = table_header_data.index('Building Name')
		table_city_index = table_header_data.index('City')
		table_state_index = table_header_data.index('State')
		table_postcode_index = table_header_data.index('Postcode')

		table_street_type = table_row_data[table_street_type_index]
		table_street_name = table_row_data[table_street_name_index]
		table_section = table_row_data[table_section_index]
		table_floor_no = table_row_data[table_floor_no_index]
		table_building_name = table_row_data[table_building_name_index]
		table_city = table_row_data[table_city_index]
		table_state = table_row_data[table_state_index]
		table_postcode = table_row_data[table_postcode_index]

		accumulated_points = 0

		# determines the number of columns, that has actual data.
		actual_data_col_counter = 0

		for table_header_index in range(len(table_header_data)):
			input_header_index = table_header_index
			while table_header_data[table_header_index] != input_header_data[input_header_index]:
				input_header_index = table_header_index + 1
			if table_header_data[table_header_index] == input_header_data[input_header_index] and input_row_data[table_header_index] != '':
				actual_data_col_counter = actual_data_col_counter + 1

		if input_house_unit_lotno == table_house_unit_lotno and input_house_unit_lotno != '':
			accumulated_points = accumulated_points + 1
		if input_street_type.upper().strip().strip() == table_street_type.upper().strip().strip() and input_street_type != '':
			accumulated_points = accumulated_points + 1
		if input_street_name.upper().strip().strip() == table_street_name.upper().strip().strip() and input_street_name != '':
			accumulated_points = accumulated_points + 1
		if input_section.upper().strip().strip() == table_section.upper().strip().strip() and input_section != '':
			accumulated_points = accumulated_points + 1
		if input_floor_no == table_floor_no and input_floor_no != '':
			accumulated_points = accumulated_points + 1
		if input_building_name.upper().strip().strip() == table_building_name.upper().strip().strip() and input_building_name != '':
			accumulated_points = accumulated_points + 1
		if input_city.upper().strip().strip() == table_city.upper().strip().strip() and input_city != '':
			accumulated_points = accumulated_points + 1
		if input_state.upper().strip().strip() == table_state.upper().strip().strip() and input_state != '':
			accumulated_points = accumulated_points + 1
		if input_postcode == table_postcode and input_postcode != '':
			accumulated_points = accumulated_points + 1

		if accumulated_points == actual_data_col_counter: ### TODO: do cases for when unit_num_match_bool is Y or N.
			return "BEST MATCH"
		else:
			return accumulated_points


def go_back_to_coverage_search_page(driver, a):
	driver.execute_script("window.history.go(-1)")
	while driver.execute_script("return document.readyState;") != "complete":
		time.sleep(0.5)

	try:
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//select[@id='actionForm_state']")))
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//select[@id='actionForm_state']")))
		return

	except TimeoutException:
		go_back_to_coverage_search_page(driver,a)


def check_coverage_and_notify(table_row_num, driver, a):

	def check_coverage_and_notify_actual(driver, a, address_string):
		try:
			while driver.execute_script("return document.readyState;") != "complete":
				time.sleep(0.5)
			WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[4]/center/div[2]/div[2]/div/table/tbody/tr[2]/td/div[2]/div/form/div[3]/div[1]/table/tbody/tr[2]/td[1]/img[contains(@src, 'tick_checkcoverage')]")))
			# coverage available.
			print("COVERAGE_AVAILABLE!!")
			send_message(address_string + " has coverage!")
			send_email(address_string + " has coverage!")
			### TODO: call telegram and email functions - and send notifications.
			go_back_to_coverage_search_page(driver, a)

		except TimeoutException:
			print("COVERAGE NOT AVAILABLE")
			send_message(address_string + " does not have coverage.")
			send_email(address_string + " does not have coverage.")
			go_back_to_coverage_search_page(driver, a)

	def bridge_to_actual_op(driver,a):
		address_string = ''
		for tab in driver.find_elements(By.XPATH, "//div[@id='fields']//table//tbody//tr[@valign='top']"):
			if tab.text != '' and tab.text != '*Kindly fill in the missing information':
				address_string = address_string + tab.text + '\n'
				# print("TAB.TEXT:", tab.text)
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

		next_button = driver.find_element(By.XPATH, "//input[@type='image' and contains(@src, 'btnNext')]")
		a.move_to_element(next_button).click().perform()

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

	
	# /html/body/div/div/div[4]/center/div[2]/div[2]/div/table/tbody/tr[2]/td/div[2]/div/form/div[3]/div[1]/table/tbody/tr[2]/td[1]/img

def input_speed_requested(driver, a):
	#inputing the "speed requested"
	speed_requested_tab = Select(driver.find_element(By.XPATH, "(//div[@class='partnerHomeContent'])[3]//select"))
	speed_requested_tab.select_by_visible_text("50Mbps and above")

	check_coverage_button = driver.find_element(By.XPATH, "//input[@type='image' and @value='Next' and @alt='submit']")
	a.move_to_element(check_coverage_button).click().perform()


def finding_coverage(driver, a):

	def select_state(driver, a):
		if state in accpeted_states_list:
			state_tab = Select(driver.find_element(By.XPATH, "//select[@id='actionForm_state']"))
			state_tab.select_by_visible_text(f"{state}")
		elif state == 'LABUAN':
			state_tab = Select(driver.find_element(By.XPATH, "//select[@id='actionForm_state']"))
			state_tab.select_by_visible_text("WILAYAH PERSEKUTUAN LABUAN")
		elif state == 'PUTRAJAYA':
			state_tab = Select(driver.find_element(By.XPATH, "//select[@id='actionForm_state']"))
			state_tab.select_by_visible_text("WILAYAH PERSEKUTUAN PUTRAJAYA")

		else:
			raise Exception(f"\n*****\n\nERROR IN ROW {row_counter} OF YOUR CSV SHEET - \n\n*****\n\
The State in ROW {row_counter} is {state}. \n\
State needs to be one of \'MELAKA\', \'KELANTAN\', \'KEDAH\', \'JOHOR\', \
\'NEGERI SEMBILAN\', \'PAHANG\', \'PERAK\', \'PERLIS\', \
\'PULAU PINANG\', \'SABAH\', \'SARAWAK\', \'SELANGOR\', \'TERENGGANU\', \
\'LABUAN\', \'PUTRAJAYA\', \
\'WILAYAH PERSEKUTUAN\', \'WILAYAH PERSEKUTUAN LABUAN\', \
\'WILAYAH PERSEKUTUAN PUTRAJAYA\'\n*****\n")

#####

	input_speed_requested(driver, a)

	# we've arrived at the coverage page.
	while driver.execute_script("return document.readyState;") != "complete":
		time.sleep(0.5)

	with open('partners_coveragecheck.csv','rt') as f: ### TODO: change this with the actual file that's input by the user.

		csvreader = csv.reader(f)

		header = []
		header = next(csvreader)
		header[0] = header[0].replace('\ufeff', '')

		house_unit_lotno_index = header.index('House/Unit/Lot No.')
		street_type_index = header.index('Street Type')
		street_name_index = header.index('Street Name')
		section_index = header.index('Section')
		floor_no_index = header.index('Floor No.')
		building_name_index = header.index('Building Name')
		city_index = header.index('City')
		state_index = header.index('State')
		postcode_index = header.index('Postcode')
		tid_option_index = header.index('tid (option)')
		source_option_index = header.index('source (option)')
		uid_index = header.index('Uid')
		result_type_index = header.index('Result type')
		result_string_index = header.index('result string')
		salesman_index = header.index('Salesman')
		email_notification_index = header.index('Email Notification')
		telegram_index = header.index('telegram')

		accpeted_states_list = ['MELAKA', 'KELANTAN', 'KEDAH', 'JOHOR', 'NEGERI SEMBILAN', 'PAHANG', 'PERAK', 'PERLIS', 
			'PULAU PINANG', 'SABAH', 'SARAWAK', 'SELANGOR', 'TERENGGANU', 'WILAYAH PERSEKUTUAN',
			'WILAYAH PERSEKUTUAN LABUAN', 'WILAYAH PERSEKUTUAN PUTRAJAYA']

		accepted_street_types_list = ['ALUR', 'OFF JALAN', 'AVENUE', 'BATU', 'BULATAN', 'CABANG', 'CERUMAN', 
			'CERUNAN', 'CHANGKAT', 'CROSS', 'DALAMAN', 'DATARAN', 'DRIVE', 'GAT', 'GELUGOR', 'GERBANG', 
			'GROVE', 'HALA', 'HALAMAN', 'HALUAN', 'HILIR', 'HUJUNG', 'JALAN', 'JAMBATAN', 'JETTY', 
			'KAMPUNG', 'KELOK', 'LALUAN', 'LAMAN', 'LANE', 'LANGGAK', 'LEBOH', 'LEBUH', 'LEBUHRAYA', 
			'LEMBAH', 'LENGKOK', 'LENGKONGAN', 'LIKU', 'LILITAN', 'LINGKARAN', 'LINGKONGAN', 
			'LINGKUNGAN', 'LINTANG', 'LINTASAN', 'LORONG', 'LOSONG', 'LURAH', 'M G', 'MAIN STREET', 
			'MEDAN', 'PARIT', 'PEKELILING', 'PERMATANG', 'PERSIARAN', 'PERSINT', 'PERSISIRAN', 'PESARA', 
			'PESIARAN', 'PIASAU', 'PINGGIAN', 'PINGGIR', 'PINGGIRAN', 'PINTAS', 'PINTASAN', 'PUNCAK', 
			'REGAT', 'ROAD', 'SEBERANG', 'SELASAR', 'SELEKOH', 'SILANG', 'SIMPANG', 'SIMPANGAN', 
			'SISIRAN', 'SLOPE', 'SOLOK', 'STREET', 'SUSUR', 'SUSURAN', 'TAMAN', 'TANJUNG', 'TEPIAN', 
			'TINGGIAN', 'TINGKAT', 'P.O.Box', 'PO Box']

		"""
		header=
		['House/Unit/Lot No.', 'Street Type', 'Street Name', 'Section', 
		'Floor No.', 'Building Name', 'City', 'State', 'Postcode', 'tid (option)', 
		'source (option)', 'Uid', 'Result type', 'result string', 'Salesman', 
		'Email Notification', 'telegram']
		"""

		"""
		example row_data:
		['A-1-1', 'JALAN', 'PS 11', 
		'PRIMA SELAYANG', '1', 'DATARAN EMERALD', 
		'BATU CAVES', 'SELANGOR', '68100', 
		'', '', '', '', '', '', '', '']
		"""

		# //form[@name='Netui_Form_1']//table//select//option[@style='width: 153px']

		data = csv.reader(f)
		row_counter = 1

		for input_row_data in data: # goes through every row of the csv file.

			row_counter = row_counter + 1

			### STEP ONE: select state.
			state = input_row_data[state_index].upper().strip()

			try:
				select_state(driver, a)

			except NoSuchElementException:
				go_back_to_coverage_search_page(driver, a)
				select_state(driver, a)

			### STEP TWO: select street type.
			street_type = input_row_data[street_type_index].upper().strip()

			if street_type in accepted_street_types_list:
				try:
					street_types_tab = Select(driver.find_element(By.XPATH, "//form[@name='Netui_Form_1']//table//select"))
					street_types_tab.select_by_visible_text(f"{street_type}")
				except NoSuchElementException:
					driver.refresh()
					while driver.execute_script("return document.readyState;") != "complete":
						time.sleep(0.5)
					street_types_tab = Select(driver.find_element(By.XPATH, "//form[@name='Netui_Form_1']//table//select"))
					street_types_tab.select_by_visible_text(f"{street_type}")
			else:
				raise Exception(f"\n*****\n\nERROR IN ROW {row_counter} OF YOUR CSV SHEET - \n\n*****\n\
The Street Type in ROW {row_conuter} is {street_type}. \n\
Street Type needs to be one of \'ALUR\', \'OFF JALAN\', \'AVENUE\', \'BATU\', \'BULATAN\', \'CABANG\', \'CERUMAN\', \
\'CERUNAN\', \'CHANGKAT\', \'CROSS\', \'DALAMAN\', \'DATARAN\', \'DRIVE\', \'GAT\', \'GELUGOR\', \'GERBANG\', \
\'GROVE\', \'HALA\', \'HALAMAN\', \'HALUAN\', \'HILIR\', \'HUJUNG\', \'JALAN\', \'JAMBATAN\', \'JETTY\', \
\'KAMPUNG\', \'KELOK\', \'LALUAN\', \'LAMAN\', \'LANE\', \'LANGGAK\', \'LEBOH\', \'LEBUH\', \'LEBUHRAYA\', \
\'LEMBAH\', \'LENGKOK\', \'LENGKONGAN\', \'LIKU\', \'LILITAN\', \'LINGKARAN\', \'LINGKONGAN\', \
\'LINGKUNGAN\', \'LINTANG\', \'LINTASAN\', \'LORONG\', \'LOSONG\', \'LURAH\', \'M G\', \'MAIN STREET\', \
\'MEDAN\', \'PARIT\', \'PEKELILING\', \'PERMATANG\', \'PERSIARAN\', \'PERSINT\', \'PERSISIRAN\', \'PESARA\', \
\'PESIARAN\', \'PIASAU\', \'PINGGIAN\', \'PINGGIR\', \'PINGGIRAN\', \'PINTAS\', \'PINTASAN\', \'PUNCAK\', \
\'REGAT\', \'ROAD\', \'SEBERANG\', \'SELASAR\', \'SELEKOH\', \'SILANG\', \'SIMPANG\', \'SIMPANGAN\', \
\'SISIRAN\', \'SLOPE\', \'SOLOK\', \'STREET\', \'SUSUR\', \'SUSURAN\', \'TAMAN\', \'TANJUNG\', \'TEPIAN\', \
\'TINGGIAN\', \'TINGKAT\', \'P.O.Box\', \'PO Box\'\n*****\n")


			### STEP THREE: select street name.
			street_name = input_row_data[street_name_index].upper()
			building_name = input_row_data[building_name_index].upper()

			space_between_word_and_num_verifier = re.search(r'([A-Z])+(\d)+', street_name)

			if space_between_word_and_num_verifier is not None:
				text_regex = re.compile(r'([A-Z])+')
				text_res = text_regex.search(street_name)
				text_in_street_name = text_res.group()

				number_regex = re.compile(r'(\d)+')
				number_res = number_regex.search(street_name)
				number_in_street_name = number_res.group()

				street_name = text_in_street_name + ' ' + number_in_street_name

			street_name_input = driver.find_element(By.XPATH, "(//form[@name='Netui_Form_1']//table//tbody//tr//td//input[@type='text'])[1]")
			street_name_input.clear()
			street_name_input.send_keys(street_name)

			if building_name != '':
				building_name_input = driver.find_element(By.XPATH, "(//div[@class='subContent']//td[@valign='top']//form[@name='Netui_Form_2']//table//tbody//tr//td//input[@type='text'])[1]")
				building_name_input.clear()
				building_name_input.send_keys(building_name)


			### STEP FOUR: click 'search'.
			search_button = driver.find_element(By.XPATH, "//form[@name='Netui_Form_1']//img[@alt='Search']")
			a.move_to_element(search_button).click().perform()

			try:
				WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//table[@id='resultAddressGrid']")))

			except TimeoutException:
				try:
					captcha_to_solve = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[@src='jcaptchaCustom.jpg' and @border='1']")))
					captcha_code = solve_captcha(captcha_elem_to_solve=captcha_to_solve, driver=driver)

					captcha_field = driver.find_element(By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//input[@type='text']")
					captcha_field.clear()
					captcha_field.send_keys(captcha_code)
					submit_captcha_button = driver.find_element(By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[contains(@src, 'btnGo')]")
					a.move_to_element(submit_captcha_button).click().perform()

				except TimeoutException:
					raise Exception("Error in step FOUR of coverage_check.py - table did not pop up after clicking 'Search'. Captcha did not pop up too.")

			### STEP FIVE: find the row that has the building name of the input address - from the results table.

			table_header_data = []
			datagrid_header = driver.find_elements(By.XPATH, "//tr[@class='datagrid-header']//th[@class='datagrid']")
			for tab in datagrid_header:
				if tab.text != '':
					table_header_data.append(tab.text)

			index_for_even = 1
			index_for_odd = 1

			points_list = []

			url_of_table = driver.current_url

			# TODO: store all of the points in a list. choose the highest that's larger than or equals to (number of columns filled - 1). if none, send notification that there's no coverage.
			### table_row_data is sometimes empty. find out why!
			for table_row_num in range(len(driver.find_elements(By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"))):
				# getting to the correct page to compare data of each row.
				retry_times = 0
				on_page = False
				if driver.find_element(By.XPATH, "//table[@id='resultAddressGrid']"):
					on_page = True
				while not on_page:
					driver.get(url_of_table)
					while driver.execute_script("return document.readyState;") != "complete":
						time.sleep(0.5)
					try:
						WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//table[@id='resultAddressGrid']")))
						on_page = True
					except TimeoutException:
						try:
							captcha_to_solve = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[@src='jcaptchaCustom.jpg' and @border='1']")))
							captcha_code = solve_captcha(captcha_elem_to_solve=captcha_to_solve, driver=driver)

							captcha_field = driver.find_element(By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//input[@type='text']")
							captcha_field.clear()
							captcha_field.send_keys(captcha_code)
							submit_captcha_button = driver.find_element(By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[contains(@src, 'btnGo')]")
							a.move_to_element(submit_captcha_button).click().perform()

						except TimeoutException:
							print("Retrying step FIVE - going back and comparing each address...")
							retry_times = retry_times + 1
							if retry_times > 5:
								raise Exception("Error in step FIVE of coverage_check.py - table did not pop up after going back. Captcha did not pop up too.")

				# actually comparing the data of each row.
				table_row_data = driver.find_elements(By.XPATH, f"(//table[@id='resultAddressGrid' and @class='datagrid']//tbody//tr[@class='odd' or @class='even'])[{table_row_num+1}]//td[@class='datagrid']")
				points = return_points_for_row(table_row_data_list=table_row_data, table_header_data=table_header_data, 
					input_row_data=input_row_data, input_header_data=header, driver=driver)
				print("POINTS_ACCUMULATED: ", points)
				if points == 'BEST MATCH':
					points_list = []
					check_coverage_and_notify(table_row_num=table_row_num, driver=driver, a=a)
					break # it's the best that we can get, so we can just break out of the loop.
				else:
					points_list.append((table_row_num, points))

			# now, there's no best match. so we take the row with the highest points.
			if len(points_list) != 0:
				# this would mean there's not a best match.
				points_list = sorted(points_list, key=lambda x: x[1])

				print("POINTS_LISTT:", points_list)

				max_point_tuple = points_list[0]

				check_coverage_and_notify(table_row_num=max_point_tuple[0], driver=driver, a=a)

