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

from PIL import Image
from operations.solve_captcha import solve_captcha
from operations.set_accepted_params import set_accepted_params

from .return_points_for_row import return_points_for_row
from .go_back_to_search_page import go_back_to_coverage_search_page
from .check_coverage_and_notify import check_coverage_and_notify
from .input_speed_requested import input_speed_requested
from current_input_row.current_input_row import CurrentInputRow


def finding_coverage(driver, a):

	def select_state(driver, a, state):
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

	script_dir = os.path.dirname(__file__)  # Script directory
	full_path = os.path.join(script_dir, '../../partners_coveragecheck.csv')

	with open(full_path,'rt') as f: ### TODO: change this with the actual file that's input by the user.

		csvreader = csv.reader(f)

		input_header_data = []
		input_header_data = next(csvreader)
		input_header_data[0] = input_header_data[0].replace('\ufeff', '')

		current_input_row = CurrentInputRow.get_instance()
		current_input_row.set_csv_file_path(self=current_input_row, csv_file_path=full_path)
		current_input_row.set_input_header_data(self=current_input_row, input_header_data=input_header_data)
		set_accepted_params()
		"""
		input_header_data=
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

		data = csv.reader(f)
		row_counter = 1

		for input_row_data in data: # goes through every row of the csv file.

			current_input_row.set_input_row_data(self=current_input_row, input_row_data=input_row_data)

			row_counter = row_counter + 1

			### STEP ONE: select state.
			state = current_input_row.get_state(self=current_input_row).upper().strip()

			try:
				select_state(driver, a, state)

			except NoSuchElementException:
				try:
					go_back_to_coverage_search_page(driver)
					select_state(driver, a, state)
				except NoSuchElementException:
					# the weird bug that only has wp as state came. skipping this address operation...
					continue

			### STEP TWO: select street type.
			street_type = current_input_row.get_street_type(self=current_input_row).upper().strip()

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
			street_name = current_input_row.get_street_name(self=current_input_row).upper()
			building_name = current_input_row.get_building_name(self=current_input_row).upper()

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
					input_row_data=input_row_data, input_header_data=input_header_data, driver=driver)
				# print("POINTS_ACCUMULATED: ", points)
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

				# print("POINTS_LISTT:", points_list)

				max_point_tuple = points_list[0]

				check_coverage_and_notify(table_row_num=max_point_tuple[0], driver=driver, a=a)

