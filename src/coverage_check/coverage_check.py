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

    def select_state(driver, a, state, accepted_states_list):
        # TODO: add condition for when there is only 'Wilayah Persekutuan' in the list.
        # if len(driver.find_elements(By.XPATH, "//select[@id='actionForm_state']//option")) == 1:
        # 	a.move_to_element(driver.find_element(By.XPATH, "//a[contains(text(), 'Help new customer')]")).click().perform()

        if state in accepted_states_list:
            state_tab = Select(driver.find_element(
                By.XPATH, "//select[@id='actionForm_state']"))
            state_tab.select_by_visible_text(f"{state}")
        elif state == 'LABUAN':
            state_tab = Select(driver.find_element(
                By.XPATH, "//select[@id='actionForm_state']"))
            state_tab.select_by_visible_text("WILAYAH PERSEKUTUAN LABUAN")
        elif state == 'PUTRAJAYA':
            state_tab = Select(driver.find_element(
                By.XPATH, "//select[@id='actionForm_state']"))
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

        to_proceed = False
        while to_proceed == False:
            try:
                captcha_to_solve = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='blockUI blockMsg blockPage']//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[@src='jcaptchaCustom.jpg' and @border='1']")))
                captcha_code = solve_captcha(
                    captcha_elem_to_solve=captcha_to_solve, driver=driver)

                captcha_field = driver.find_element(
                    By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//input[@type='text']")
                captcha_field.clear()
                captcha_field.send_keys(captcha_code)
                submit_captcha_button = driver.find_element(
                    By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[contains(@src, 'btnGo')]")
                a.move_to_element(submit_captcha_button).click().perform()

                try:
                    WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                        (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

                except TimeoutException:
                    to_proceed = True

            except TimeoutException:
                # no captcha to solve.
                to_proceed = True

    def iterate_through_all_and_notify(driver, a, filtered):
        """
        this function 
        1. gets to the actual results page, 
        2. iterates through all the results, and 
        3. calculates the points of every results
        4. and calls "check_coverage_and_notify()" with the best result row.

        NOTE: the table_row_num starts from 0. that is, 0 is the first row of a result in the result table.
        """
        points_list = []
        table_header_data = []

        if filtered == False:
            # block for when there is only one result in the table.
            if (len(driver.find_elements(By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"))) == 1:
                check_coverage_and_notify(
                    table_row_num=0, driver=driver, a=a, filtered=filtered)

            x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"

        else:
            x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]"

        for table_row_num in range(len(driver.find_elements(By.XPATH, x_code_path))):
            # getting to the correct page to compare data of each row.
            retry_times = 0
            on_page = False
            if driver.find_element(By.XPATH, "//table[@id='resultAddressGrid']"):
                # if the results table actually exists, then on_page = True
                on_page = True

            while not on_page:  # to get to the actual table results page.
                driver.get(driver.current_url)
                while driver.execute_script("return document.readyState;") != "complete":
                    time.sleep(0.5)
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                        (By.XPATH, "//table[@id='resultAddressGrid']")))
                    on_page = True
                except TimeoutException:
                    to_proceed = False
                    while to_proceed == False:
                        try:
                            captcha_to_solve = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                                (By.XPATH, "//div[@class='blockUI blockMsg blockPage']//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[@src='jcaptchaCustom.jpg' and @border='1']")))
                            captcha_code = solve_captcha(
                                captcha_elem_to_solve=captcha_to_solve, driver=driver)

                            captcha_field = driver.find_element(
                                By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//input[@type='text']")
                            captcha_field.clear()
                            captcha_field.send_keys(captcha_code)
                            submit_captcha_button = driver.find_element(
                                By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[contains(@src, 'btnGo')]")
                            a.move_to_element(
                                submit_captcha_button).click().perform()

                            try:
                                WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                                    (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

                            except TimeoutException:
                                to_proceed = True

                        except TimeoutException:
                            print(
                                "Retrying step FIVE - going back and comparing each address...")
                            retry_times = retry_times + 1
                            if retry_times > 5:
                                raise Exception(
                                    "Error in step FIVE of coverage_check.py - table did not pop up after going back. Captcha did not pop up too.")

            if len(table_header_data) == 0:
                datagrid_header = driver.find_elements(
                    By.XPATH, "//tr[@class='datagrid-header']//th[@class='datagrid']")
                for tab in datagrid_header:
                    if tab.text != '':
                        table_header_data.append(tab.text)

            # actually comparing the data of each row.
            table_row_data = driver.find_elements(
                By.XPATH, f"({x_code_path})[{table_row_num+1}]//td[@class='datagrid']")
            points = return_points_for_row(table_row_data_list=table_row_data, table_header_data=table_header_data,
                                           input_row_data=input_row_data, input_header_data=input_header_data, driver=driver)
            if points == 'BEST MATCH':
                points_list = []
                check_coverage_and_notify(
                    table_row_num=table_row_num, driver=driver, a=a, filtered=filtered)
                # it's the best that we can get, so we can just break out of the loop.
                break
            else:
                points_list.append((table_row_num, points))

        # now, there's no best match. so we take the row with the highest points.
        if len(points_list) != 0:
            # this would mean there's not a best match.
            points_list = sorted(points_list, key=lambda x: x[1])

            max_point_tuple = points_list[0]

            check_coverage_and_notify(
                table_row_num=max_point_tuple[0], driver=driver, a=a, filtered=filtered)

    def search_using_street_type_and_name(driver, a):
        unit_lotno = current_input_row.get_house_unit_lotno(
            self=current_input_row).strip()
        street_type = current_input_row.get_street_type(
            self=current_input_row).strip()
        street_name = current_input_row.get_street_name(
            self=current_input_row).strip()

        keyword_search_string = ''
        if len(unit_lotno) > 0:
            keyword_search_string = keyword_search_string + unit_lotno + ' '
        keyword_search_string = keyword_search_string + \
            street_type + ' ' + street_name + ' ' + building_name

        keyword_field = driver.find_element(
            By.XPATH, "//form[@name='Netui_Form_3']//input[@type='text' and contains(@name, 'searchString')]")
        keyword_field.clear()
        keyword_field.send_keys(keyword_search_string)

        search_btn_third_col = driver.find_element(
            By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
        a.move_to_element(search_btn_third_col).click().perform()

        # yes it is.
        # solve captcha

        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//table[@id='resultAddressGrid']")))

        except TimeoutException:
            to_proceed = False
            while to_proceed == False:
                try:
                    captcha_to_solve = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='blockUI blockMsg blockPage']//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[@src='jcaptchaCustom.jpg' and @border='1']")))
                    captcha_code = solve_captcha(
                        captcha_elem_to_solve=captcha_to_solve, driver=driver)

                    captcha_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//input[@type='text']")))
                    captcha_field.clear()
                    captcha_field.send_keys(captcha_code)
                    submit_captcha_button = driver.find_element(
                        By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[contains(@src, 'btnGo')]")
                    a.move_to_element(submit_captcha_button).click().perform()

                    try:
                        WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                            (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

                    except TimeoutException:
                        to_proceed = True
                        # break

                except TimeoutException:
                    raise Exception(
                        "Error in the SEARCHING step of coverage_check.py - table did not pop up after clicking 'Search'. Captcha did not pop up too.")

            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//table[@id='resultAddressGrid']")))

        iterate_through_all_and_notify(driver, a, filtered=False)

    def get_street_type_and_search(driver, a, accepted_street_types_list):
        if current_input_row.get_street_type(self=current_input_row).upper().strip() not in accepted_street_types_list:
            raise Exception(f"\n*****\n\nERROR IN ROW {row_counter} OF YOUR CSV SHEET - \n\n*****\n\
The Street Type in ROW {row_counter} is {current_input_row.get_street_type(self=current_input_row)}. \n\
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
        else:
            search_using_street_type_and_name(driver, a)
#####

    input_speed_requested(driver, a)

    # we've arrived at the coverage page.
    while driver.execute_script("return document.readyState;") != "complete":
        time.sleep(0.5)

    script_dir = os.path.dirname(__file__)  # Script directory
    full_path = os.path.join(script_dir, '../../second_jaco.csv')

    # TODO: change this with the actual file that's input by the user.
    with open(full_path, 'rt') as f:

        csvreader = csv.reader(f)

        input_header_data = []
        input_header_data = next(csvreader)
        input_header_data[0] = input_header_data[0].replace('\ufeff', '')

        current_input_row = CurrentInputRow.get_instance()
        current_input_row.set_csv_file_path(
            self=current_input_row, csv_file_path=full_path)
        current_input_row.set_input_header_data(
            self=current_input_row, input_header_data=input_header_data)
        set_accepted_params()

        accepted_states_list = current_input_row.get_accepted_states_list(
            self=current_input_row)
        accepted_street_types_list = current_input_row.get_accepted_street_types_list(
            self=current_input_row)
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

        for input_row_data in data:  # goes through every row of the csv file.

            current_input_row.set_input_row_data(
                self=current_input_row, input_row_data=input_row_data)

            row_counter = row_counter + 1

            # STEP ONE: select state.
            state = current_input_row.get_state(
                self=current_input_row).upper().strip()

            try:
                select_state(driver, a, state, accepted_states_list)

            except NoSuchElementException:
                # THIS EXCEPTION is what we mean:
                # selenium.common.exceptions.NoSuchElementException: Message: Could not locate element with visible text: SELANGOR
                try:
                    go_back_to_coverage_search_page(driver)
                    select_state(driver, a, state, accepted_states_list)
                except NoSuchElementException:
                    # THIS EXCEPTION is what we mean:
                    # selenium.common.exceptions.NoSuchElementException: Message: Could not locate element with visible text: SELANGOR
                    # the weird bug that only has wp as state came. skipping this address operation...
                    continue

            # STEP TWO: set up the search string.
            keyword_search_string = ''

            # STEP TWO A: find if there's a building name.
            building_name = current_input_row.get_building_name(
                self=current_input_row).strip()
            if building_name != '':
                keyword_search_string = keyword_search_string + building_name

                keyword_field = driver.find_element(
                    By.XPATH, "//form[@name='Netui_Form_3']//input[@type='text' and contains(@name, 'searchString')]")
                keyword_field.clear()
                keyword_field.send_keys(keyword_search_string)

                search_btn_third_col = driver.find_element(
                    By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
                a.move_to_element(search_btn_third_col).click().perform()

                # wait for the results table to pop up.
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                        (By.XPATH, "//table[@id='resultAddressGrid']")))
                except TimeoutException:
                    to_proceed = False
                    while to_proceed == False:
                        try:
                            captcha_to_solve = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                                (By.XPATH, "//div[@class='blockUI blockMsg blockPage']//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[@src='jcaptchaCustom.jpg' and @border='1']")))
                            captcha_code = solve_captcha(
                                captcha_elem_to_solve=captcha_to_solve, driver=driver)

                            captcha_field = driver.find_element(
                                By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//input[@type='text']")
                            captcha_field.clear()
                            captcha_field.send_keys(captcha_code)
                            submit_captcha_button = driver.find_element(
                                By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[contains(@src, 'btnGo')]")
                            a.move_to_element(
                                submit_captcha_button).click().perform()

                            try:
                                WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                                    (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

                            except TimeoutException:
                                to_proceed = True

                        except TimeoutException:
                            raise Exception(
                                "Error in the enter BUILDING NAME step of coverage_check.py - table did not pop up after clicking 'Search'. Captcha did not pop up too.")

                WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, "//table[@id='resultAddressGrid']")))

                number_of_results = len(driver.find_elements(
                    By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"))

                if number_of_results == 0:
                    get_street_type_and_search(
                        driver, a, accepted_street_types_list)

                elif number_of_results > 50:
                    unit_no_filter_tab = driver.find_element(
                        By.XPATH, "//input[@id='flt0_resultAddressGrid' and @type='text' and @class='flt']")
                    unit_no_filter_tab.clear()
                    current_input_row = CurrentInputRow.get_instance()
                    unit_no_filter_tab.send_keys(current_input_row.get_house_unit_lotno(
                        self=current_input_row).strip())  # entering the unit number so that we can reduce the num of results.

                    # assuming that the number of results have been significantly reduced.
                    iterate_through_all_and_notify(driver, a, filtered=True)
                    # TODO: implement this for filtered. the main difference is the xpath. bse it on iterate_through_all_and_notify

                else:
                    iterate_through_all_and_notify(driver, a, filtered=False)

            else:
                print("BUILDING NAME EMPTY. SO WE ENTER STREET STUFF INTO KEYWORD TAB.")
                get_street_type_and_search(
                    driver, a, accepted_street_types_list)

            # ### STEP THREE: select street name.
            # street_name = current_input_row.get_street_name(self=current_input_row).upper()
            # building_name = current_input_row.get_building_name(self=current_input_row).upper()

            # space_between_word_and_num_verifier = re.search(r'([A-Z])+(\d)+', street_name)

            # if space_between_word_and_num_verifier is not None:
            # 	text_regex = re.compile(r'([A-Z])+')
            # 	text_res = text_regex.search(street_name)
            # 	text_in_street_name = text_res.group()

            # 	number_regex = re.compile(r'(\d)+')
            # 	number_res = number_regex.search(street_name)
            # 	number_in_street_name = number_res.group()

            # 	street_name = text_in_street_name + ' ' + number_in_street_name

            # street_name_input = driver.find_element(By.XPATH, "(//form[@name='Netui_Form_1']//table//tbody//tr//td//input[@type='text'])[1]")
            # street_name_input.clear()
            # street_name_input.send_keys(street_name)

            # if building_name != '':
            # 	building_name_input = driver.find_element(By.XPATH, "(//div[@class='subContent']//td[@valign='top']//form[@name='Netui_Form_2']//table//tbody//tr//td//input[@type='text'])[1]")
            # 	building_name_input.clear()
            # 	building_name_input.send_keys(building_name)

            # ### STEP FOUR: click 'search'.
            # search_button = driver.find_element(By.XPATH, "//form[@name='Netui_Form_1']//img[@alt='Search']")
            # a.move_to_element(search_button).click().perform()

            # try:
            # 	WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//table[@id='resultAddressGrid']")))

            # except TimeoutException:
            # 	try:
            # 		captcha_to_solve = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[@src='jcaptchaCustom.jpg' and @border='1']")))
            # 		captcha_code = solve_captcha(captcha_elem_to_solve=captcha_to_solve, driver=driver)

            # 		captcha_field = driver.find_element(By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//input[@type='text']")
            # 		captcha_field.clear()
            # 		captcha_field.send_keys(captcha_code)
            # 		submit_captcha_button = driver.find_element(By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[contains(@src, 'btnGo')]")
            # 		a.move_to_element(submit_captcha_button).click().perform()

            # 	except TimeoutException:
            # 		raise Exception("Error in step FOUR of coverage_check.py - table did not pop up after clicking 'Search'. Captcha did not pop up too.")

            # ### STEP FIVE: find the row that has the building name of the input address - from the results table.

            # index_for_even = 1
            # index_for_odd = 1

            # points_list = []

            # url_of_table = driver.current_url

            # # TODO: store all of the points in a list. choose the highest that's larger than or equals to (number of columns filled - 1). if none, send notification that there's no coverage.
            # ### table_row_data is sometimes empty. find out why!
