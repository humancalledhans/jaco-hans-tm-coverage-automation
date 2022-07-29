from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

import time
from src.singleton.cvg_task import CVGTask
from src.singleton.data_id_range import DataIdRange
from src.notifications.email_msg import send_email
from src.notifications.telegram_msg import send_message

from src.operations.solve_captcha import solve_captcha
from src.operations.set_accepted_params import set_accepted_params

from .return_points_for_row import return_points_for_row
from .go_back_to_search_page import go_back_to_coverage_search_page
from .check_coverage_and_notify import check_coverage_and_notify
from .input_speed_requested import input_speed_requested
from src.singleton.current_input_row import CurrentInputRow
from src.db_read_write.db_write_address import write_or_edit_result
from src.db_read_write.db_read_address import read_from_db
from src.db_read_write.db_get_chat_id import get_chat_id


class FindingCoverage:

    # __instance = None

    # @staticmethod
    # def get_instance():
    #     if FindingCoverage.__instance == None:
    #         FindingCoverage()
    #     return FindingCoverage.__instance

    # def __init__(self):
    #     if FindingCoverage.__instance != None:
    #         raise Exception(
    #             "FindingCoverage instance cannot be instantiated more than once!")
    #     else:
    #         FindingCoverage.__instance = self

    # def get_instance(self):
    #     return self

    def __init__(self):
        pass

    def search_using_street_type_and_name(self, driver, a):
        current_input_row = CurrentInputRow.get_instance()

        unit_lotno = current_input_row.get_house_unit_lotno(
            self=current_input_row).strip()
        street = current_input_row.get_street(
            self=current_input_row).strip()

        keyword_search_string = ''
        if len(unit_lotno) > 0:  # ie: if unit_lotno exists
            keyword_search_string = keyword_search_string + unit_lotno + ' '
        keyword_search_string = keyword_search_string + \
            street

        keyword_field = driver.find_element(
            By.XPATH, "//form[@name='Netui_Form_3']//input[@type='text' and contains(@name, 'searchString')]")
        keyword_field.clear()
        keyword_field.send_keys(keyword_search_string)

        search_btn_third_col = driver.find_element(
            By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
        a.move_to_element(search_btn_third_col).click().perform()

        # solve captcha

        try:
            while driver.execute_script("return document.readyState;") != "complete":
                time.sleep(0.5)
            WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                (By.XPATH, "//table[@id='resultAddressGrid']")))

        except TimeoutException:
            to_proceed = False
            while to_proceed == False:
                try:
                    while driver.execute_script("return document.readyState;") != "complete":
                        time.sleep(0.5)
                    captcha_to_solve = WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
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
                        while driver.execute_script("return document.readyState;") != "complete":
                            time.sleep(0.5)
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                            (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

                    except TimeoutException:
                        to_proceed = True
                        # break

                except TimeoutException:
                    # TODO: re run the search for this particular id.
                    current_input_row = CurrentInputRow.get_instance()
                    current_row_id = current_input_row.get_id(
                        self=current_input_row)
                    data_id_range = DataIdRange.get_instance()
                    data_id_end = data_id_range.get_end_id(self=data_id_range)
                    self.finding_coverage(
                        driver, a, data_id_start=current_row_id, data_id_end=data_id_end)
                    raise Exception(
                        "Error in the SEARCHING step of coverage_check.py - table did not pop up after clicking 'Search'. Captcha did not pop up too.")

            while driver.execute_script("return document.readyState;") != "complete":
                time.sleep(0.5)

            WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                (By.XPATH, "//table[@id='resultAddressGrid']")))

        return (driver, a)

    def iterate_through_all_and_notify(self, driver, a, filtered, lot_no_detail_flag, building_name_found, street_name_found):
        """
        this function
        1. gets to the actual results page,
        2. iterates through all the results, and
        3. calculates the points of every results
        4. and calls "check_coverage_and_notify()" with the best result row.

        NOTE: 'building_name_found' means the building name is found in the results page.
        NOTE: the table_row_num starts from 0. that is, 0 is the first row of a result in the result table.
        """
        current_input_row = CurrentInputRow.get_instance()
        current_row_id = current_input_row.get_id(self=current_input_row)

        points_list = []
        table_header_data = []

        checked = False

        if filtered == False:
            # block for when there is only one result in the table.
            # wait for the elements in the table to come out.
            if (len(driver.find_elements(By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"))) == 1:
                check_coverage_and_notify(
                    table_row_num=0, driver=driver, a=a, filtered=filtered)
                checked = True
                return

            x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"

        else:
            x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]"

        if len(driver.find_elements(By.XPATH, x_code_path)) == 0:
            write_or_edit_result(
                id=current_row_id, result_type=8, result_text="No results.")
            go_back_to_coverage_search_page(driver, a)
            return

        for table_row_num in range(len(driver.find_elements(By.XPATH, x_code_path))):
            # getting to the correct page to compare data of each row.
            retry_times = 0
            on_page = False
            if driver.find_element(By.XPATH, "//table[@id='resultAddressGrid']"):
                # if the results table actually exists, then on_page = True
                on_page = True

            while not on_page:  # to get to the actual table results page.
                driver.get(driver.current_url)
                try:
                    while driver.execute_script("return document.readyState;") != "complete":
                        time.sleep(0.5)
                    WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                        (By.XPATH, "//table[@id='resultAddressGrid']")))
                    on_page = True
                except TimeoutException:
                    # maybe captcha is here. Let's try to solve it.
                    to_proceed = False
                    while to_proceed == False:
                        try:
                            while driver.execute_script("return document.readyState;") != "complete":
                                time.sleep(0.5)
                            captcha_to_solve = WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
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
                                while driver.execute_script("return document.readyState;") != "complete":
                                    time.sleep(0.5)
                                WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                                    (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

                            except TimeoutException:
                                to_proceed = True

                        except TimeoutException:
                            # print(
                            #     "Retrying step FIVE - going back and comparing each address...")
                            retry_times = retry_times + 1
                            if retry_times > 5:
                                raise Exception(
                                    "Error in step FIVE of coverage_check.py - table did not pop up after going back. Captcha did not pop up too.")

            if len(table_header_data) == 0:
                # to assemble the header of the results table.
                datagrid_header = driver.find_elements(
                    By.XPATH, "//tr[@class='datagrid-header']//th[@class='datagrid']")
                for tab in datagrid_header:
                    if tab.text != '':
                        table_header_data.append(tab.text)

            # actually comparing the data of each row.
            table_row_data = driver.find_elements(
                By.XPATH, f"({x_code_path})[{table_row_num+1}]//td[@class='datagrid']")
            points = return_points_for_row(
                table_row_data_list=table_row_data, table_header_data=table_header_data)

            # if the boolean value is 1, we NEED to return BEST MATCH.
            # else if the boolean value if 0, we just get the highest points.
            # print("POINTS: ", points)
            if points == 'BEST MATCH':
                points_list = []
                check_coverage_and_notify(
                    table_row_num=table_row_num, driver=driver, a=a, filtered=filtered)
                checked = True
                # it's the best that we can get, so we can just break out of the loop.
                break
            else:
                points_list.append((table_row_num, points))

        # now, there's no best match. so we take the row with the highest points.
        if checked == False:
            if lot_no_detail_flag == 0:
                # print("WENT INTO LOT_NO_DETAIL_FLAG == 0")
                # print("LEN_POINTS_LIST", len(points_list))
                if len(points_list) != 0:
                    # this would mean there's not a best match.
                    points_list = sorted(points_list, key=lambda x: x[1])

                    max_point_tuple = points_list[0]

                    check_coverage_and_notify(
                        table_row_num=max_point_tuple[0], driver=driver, a=a, filtered=filtered)
                    checked = True
            elif lot_no_detail_flag == 1:
                # lot_no_detail_flag == 1.
                # print("WENT INTO LOT_NO_DETAIL_FLAG == 1")
                # print("BUILDING_NAME_FOUND", building_name_found)
                # print("STREET_NAME_FOUND", street_name_found)

                if building_name_found == True and street_name_found == False:
                    write_or_edit_result(id=current_row_id, result_type=2,
                                         result_text="Building Name Found, Lot No Not Found.")
                    go_back_to_coverage_search_page(driver, a)
                    return
                elif building_name_found == False and street_name_found == True:
                    write_or_edit_result(id=current_row_id, result_type=3,
                                         result_text="Street Name Found, Lot No Not Found.")
                    go_back_to_coverage_search_page(driver, a)
                    return

                elif building_name_found == False and street_name_found == False:
                    # we need to match the lot no, but we couldn't. The building name was also not found. So we output "NO MATCH".
                    write_or_edit_result(
                        id=current_row_id, result_type=8, result_text="No results.")
                    go_back_to_coverage_search_page(driver, a)
                    return

    def select_state(self, driver, a, state):
        # TODO: add condition for when there is only 'Wilayah Persekutuan' in the list.
        # if len(driver.find_elements(By.XPATH, "//select[@id='actionForm_state']//option")) == 1:
        # 	a.move_to_element(driver.find_element(By.XPATH, "//a[contains(text(), 'Help new customer')]")).click().perform()

        to_proceed = False
        while to_proceed == False:
            while driver.execute_script("return document.readyState;") != "complete":
                time.sleep(0.5)
            try:
                captcha_to_solve = WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
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
                    while driver.execute_script("return document.readyState;") != "complete":
                        time.sleep(0.5)
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                        (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

                except TimeoutException:
                    to_proceed = True

            except TimeoutException:
                # no captcha to solve.
                to_proceed = True

        current_input_row = CurrentInputRow.get_instance()
        accepted_states_list = current_input_row.get_accepted_states_list(
            self=current_input_row)
        current_row_id = current_input_row.get_id(self=current_input_row)

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
            raise Exception(f"\n*****\n\nERROR IN id {current_row_id} OF DATABASE - \n\n*****\n\
The State in ROW {current_row_id} is {state}. \n\
State needs to be one of \'MELAKA\', \'KELANTAN\', \'KEDAH\', \'JOHOR\', \
\'NEGERI SEMBILAN\', \'PAHANG\', \'PERAK\', \'PERLIS\', \
\'PULAU PINANG\', \'SABAH\', \'SARAWAK\', \'SELANGOR\', \'TERENGGANU\', \
\'LABUAN\', \'PUTRAJAYA\', \
\'WILAYAH PERSEKUTUAN\', \'WILAYAH PERSEKUTUAN LABUAN\', \
\'WILAYAH PERSEKUTUAN PUTRAJAYA\'\n*****\n")

        to_proceed = False
        while to_proceed == False:
            try:
                while driver.execute_script("return document.readyState;") != "complete":
                    time.sleep(0.5)

                captcha_to_solve = WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
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
                    while driver.execute_script("return document.readyState;") != "complete":
                        time.sleep(0.5)
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                        (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

                except TimeoutException:
                    to_proceed = True

            except TimeoutException:
                # no captcha to solve.
                to_proceed = True

    def finding_coverage(self, driver, a, data_id_start, data_id_end):

        input_speed_requested(driver, a, 50)

        # we've arrived at the coverage page.
        while driver.execute_script("return document.readyState;") != "complete":
            time.sleep(0.5)

        # script_dir = os.path.dirname(__file__)  # Script directory
        # full_path = os.path.join(script_dir, '../../second_jaco.csv')

        # with open(full_path, 'rt') as f:

            # csvreader = csv.reader(f)

            # input_header_data = []
            # input_header_data = next(csvreader)
            # input_header_data[0] = input_header_data[0].replace('\ufeff', '')

        set_accepted_params()

        # data = csv.reader(f)

        # goes through every row of the database address.
        for data_id in range(data_id_start, data_id_end+1):

            read_from_db(data_id)

            # print("DATA_ID", data_id)
            current_input_row = CurrentInputRow.get_instance()
            current_row_id = current_input_row.get_id(self=current_input_row)

            # if the 'is_active' column is 0, then we skip this row.
            if current_input_row.get_is_active(self=current_input_row) == 0:
                continue

            # setting the cvg_task data for current address row id.
            cvg_task = CVGTask.get_instance()
            cvg_task.set_current_id_address_being_checked(
                current_id=current_row_id)
            cvg_task.increment_current_number_of_addresses_checked()

            # STEP ONE: select state.
            state = current_input_row.get_state(
                self=current_input_row).upper().strip()

            state_selected = False
            retry_count = 0
            while state_selected == False:
                try:
                    while driver.execute_script("return document.readyState;") != "complete":
                        time.sleep(0.5)
                    self.select_state(driver, a, state)
                    state_selected = True

                except NoSuchElementException:
                    help_new_customer_link = driver.find_element(
                        By.XPATH, "//div[@class='wlp-bighorn-window-content']//td[@align='right']//a")
                    a.move_to_element(help_new_customer_link).click().perform()
                    self.finding_coverage(
                        driver, a, data_id_start=data_id, data_id_end=data_id_end)
                    continue

            if state_selected == False:
                help_new_customer_link = driver.find_element(
                    By.XPATH, "//div[@class='wlp-bighorn-window-content']//td[@align='right']//a")
                a.move_to_element(help_new_customer_link).click().perform()
                self.finding_coverage(
                    driver, a, data_id_start=data_id, data_id_end=data_id_end)
                continue

            # THIS EXCEPTION is what we mean:
            # selenium.common.exceptions.NoSuchElementException: Message: Could not locate element with visible text: SELANGOR

            # STEP TWO: set up the search string.
            keyword_search_string = ''

            # STEP TWO A: find if there's a building name.

            lot_no_detail_flag = current_input_row.get_search_level_flag(
                self=current_input_row)
            # 0 means don't need to match lot number.
            # 1 means need to match lot number. Allows for cases like 'Building/Street name found, lot number not found'
            # refer to code in iterate_through_all_and_notify(). block where checked==False

            building_name = current_input_row.get_building(
                self=current_input_row)

            if building_name is not None:
                building_name = building_name.strip()

            if building_name != '' and building_name is not None and len(building_name) > 3:

                # get the building name, and search the results using that query.

                keyword_search_string = keyword_search_string + building_name

                keyword_field = driver.find_element(
                    By.XPATH, "//form[@name='Netui_Form_3']//input[@type='text' and contains(@name, 'searchString')]")

                keyword_field.clear()
                keyword_field.send_keys(keyword_search_string)

                search_btn_third_col = driver.find_element(
                    By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
                a.move_to_element(search_btn_third_col).click().perform()

                # building name is input.

                # wait for the results table to pop up.
                try:
                    while driver.execute_script("return document.readyState;") != "complete":
                        time.sleep(0.5)
                    WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                        (By.XPATH, "//table[@id='resultAddressGrid']")))
                except TimeoutException:
                    to_proceed = False
                    while to_proceed == False:
                        try:
                            while driver.execute_script("return document.readyState;") != "complete":
                                time.sleep(0.5)
                            captcha_to_solve = WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
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
                                while driver.execute_script("return document.readyState;") != "complete":
                                    time.sleep(0.5)
                                WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                                    (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

                            except TimeoutException:
                                to_proceed = True

                        except TimeoutException:
                            raise Exception(
                                "Error in the enter BUILDING NAME step of coverage_check.py - table did not pop up after clicking 'Search'. Captcha did not pop up too.")

                # captcha should be solved now. getting the results...
                while driver.execute_script("return document.readyState;") != "complete":
                    time.sleep(0.5)
                try:
                    WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                        (By.XPATH, "//table[@id='resultAddressGrid']")))

                    number_of_results = len(driver.find_elements(
                        By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"))

                    if number_of_results == 0:
                        number_of_results = len(driver.find_elements(
                            By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"))

                    if number_of_results > 50:
                        if lot_no_detail_flag == 0:
                            unit_no_filter_tab = driver.find_element(
                                By.XPATH, "//input[@id='flt0_resultAddressGrid' and @type='text' and @class='flt']")
                            unit_no_filter_tab.clear()
                            current_input_row = CurrentInputRow.get_instance()
                            unit_no_filter_tab.send_keys(current_input_row.get_house_unit_lotno(
                                self=current_input_row).strip())
                            # making sure the filtered resutls pop out, before we proceed.
                            try:
                                WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                                    (By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")))
                            except TimeoutException:
                                if len(driver.find_elements(By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")) == 0:
                                    replace_bool = False
                                    if "KONDOMINIUM" in keyword_search_string.upper():
                                        keyword_search_string = keyword_search_string.replace(
                                            "KONDOMINIUM", "CONDOMINIUM")
                                        replace_bool = True
                                    elif "KONDO" in keyword_search_string.upper():
                                        keyword_search_string = keyword_search_string.replace(
                                            "KONDO", "CONDO")
                                        replace_bool = True
                                    elif "JLN" in keyword_search_string.upper():
                                        keyword_search_string = keyword_search_string.replace(
                                            "JLN", "JALAN")
                                    if replace_bool:
                                        keyword_field = driver.find_element(
                                            By.XPATH, "//form[@name='Netui_Form_3']//input[@type='text' and contains(@name, 'searchString')]")

                                        keyword_field.clear()
                                        keyword_field.send_keys(
                                            keyword_search_string)

                                        search_btn_third_col = driver.find_element(
                                            By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
                                        a.move_to_element(
                                            search_btn_third_col).click().perform()

                                    # this would be the correct xpath, as we have filtered using the lot number.
                                    number_of_results = len(driver.find_elements(
                                        By.XPATH, "//tr[@class='odd' or @class='even'][not(@style)]"))

                                    if number_of_results == 0:
                                        (driver, a) = self.search_using_street_type_and_name(
                                            driver=driver, a=a)

                                        number_of_results = len(driver.find_elements(
                                            By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"))

                                        if number_of_results == 0:
                                            number_of_results = len(driver.find_elements(
                                                By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"))

                                        if number_of_results == 0:
                                            write_or_edit_result(
                                                id=current_row_id, result_type=8, result_text="No results.")
                                            go_back_to_coverage_search_page(
                                                driver, a)
                                            continue

                                        else:
                                            self.iterate_through_all_and_notify(
                                                driver, a, filtered=False, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
                                            continue

                                else:
                                    self.iterate_through_all_and_notify(
                                        driver, a, filtered=True, lot_no_detail_flag=0, building_name_found=True, street_name_found=False)
                                    continue

                            self.iterate_through_all_and_notify(
                                driver, a, filtered=True, lot_no_detail_flag=0, building_name_found=True, street_name_found=False)
                            continue

                        elif lot_no_detail_flag == 1:
                            unit_no_filter_tab = driver.find_element(
                                By.XPATH, "//input[@id='flt0_resultAddressGrid' and @type='text' and @class='flt']")
                            unit_no_filter_tab.clear()
                            current_input_row = CurrentInputRow.get_instance()
                            unit_no_filter_tab.send_keys(current_input_row.get_house_unit_lotno(
                                self=current_input_row).strip())

                            # making sure the filtered resutls pop out, before we proceed.
                            try:
                                WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                                    (By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")))
                            except TimeoutException:
                                if len(driver.fing_elements(By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")) == 0:
                                    write_or_edit_result(
                                        id=current_row_id, result_type=8, result_text="No results.")
                                    go_back_to_coverage_search_page(driver, a)
                                    continue
                                else:
                                    self.iterate_through_all_and_notify(
                                        driver, a, filtered=True, lot_no_detail_flag=1, building_name_found=True, street_name_found=False)

                            # assuming that the number of results have been significantly reduced.
                            # print("END BLOCK! OUTPUT CASE 2 OR 1 PLEASE!")
                            self.iterate_through_all_and_notify(
                                driver, a, filtered=True, lot_no_detail_flag=1, building_name_found=True, street_name_found=False)
                            continue

                    elif number_of_results == 0:
                        # no results found. so we'll try with the "condominium" instead of the "kondominium" variation things.

                        replace_bool = False
                        if "KONDOMINIUM" in keyword_search_string.upper():
                            keyword_search_string = keyword_search_string.replace(
                                "KONDOMINIUM", "CONDOMINIUM")
                            replace_bool = True
                        elif "KONDO" in keyword_search_string.upper():
                            keyword_search_string = keyword_search_string.replace(
                                "KONDO", "CONDO")
                            replace_bool = True
                        elif "JLN" in keyword_search_string.upper():
                            keyword_search_string = keyword_search_string.replace(
                                "JLN", "JALAN")
                            replace_bool = True

                        if replace_bool == True:
                            keyword_field = driver.find_element(
                                By.XPATH, "//form[@name='Netui_Form_3']//input[@type='text' and contains(@name, 'searchString')]")

                            keyword_field.clear()
                            keyword_field.send_keys(keyword_search_string)

                            search_btn_third_col = driver.find_element(
                                By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
                            a.move_to_element(
                                search_btn_third_col).click().perform()

                            number_of_results = len(driver.find_elements(
                                By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"))

                            if number_of_results == 0:
                                number_of_results = len(driver.find_elements(
                                    By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"))

                            # print(
                            #     "NUMBER_OF_RESULTS_AFTER_REPLACING JLN and KONDOMINIUM", number_of_results)

                        else:
                            # betul betul takde results.
                            # END BLOCK, OUTPUT CASE 8.

                            (driver, a) = self.search_using_street_type_and_name(
                                driver=driver, a=a)

                            number_of_results = len(driver.find_elements(
                                By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"))

                            if number_of_results == 0:
                                number_of_results = len(driver.find_elements(
                                    By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"))

                            if number_of_results == 0:
                                write_or_edit_result(
                                    id=current_row_id, result_type=8, result_text="No results.")
                                go_back_to_coverage_search_page(driver, a)
                                continue

                            else:
                                self.iterate_through_all_and_notify(
                                    driver, a, filtered=False, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
                                continue
                    else:
                        # the block where 1 < num_of_results < 50
                        if lot_no_detail_flag == 0:
                            self.iterate_through_all_and_notify(
                                driver, a, filtered=False, lot_no_detail_flag=0, building_name_found=True, street_name_found=False)
                            continue

                        else:
                            # print("END BLOCK! OUTPUT CASE 2 OR 1 PLEASE!")
                            self.iterate_through_all_and_notify(
                                driver, a, filtered=False, lot_no_detail_flag=1, building_name_found=True, street_name_found=False)
                            continue
                except TimeoutException:
                    raise Exception("Results table did not pop up.")
            else:
                # when building name is empty. do the same but for street.

                # get street_type_and_search() gets the lot no, street type, and street name - puts it tgt and searches.
                # the results table would then be there.
                # then, it calls iterate_through_all_and_notify().

                current_row_street = current_input_row.get_street(
                    self=current_input_row)

                if len(current_row_street) > 3 and 'NA' not in current_row_street.upper() and 'N/A' not in current_row_street.upper():
                    keyword_search_string = ''
                    keyword_search_string = keyword_search_string + \
                        current_row_street

                else:
                    keyword_search_string = ''
                    keyword_search_string = keyword_search_string + \
                        current_input_row.get_section(self=current_input_row)

                keyword_field = driver.find_element(
                    By.XPATH, "//form[@name='Netui_Form_3']//input[@type='text' and contains(@name, 'searchString')]")
                keyword_field.clear()
                keyword_field.send_keys(keyword_search_string)

                search_btn_third_col = driver.find_element(
                    By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
                a.move_to_element(search_btn_third_col).click().perform()

                # solve captcha

                try:
                    while driver.execute_script("return document.readyState;") != "complete":
                        time.sleep(0.5)
                    WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                        (By.XPATH, "//table[@id='resultAddressGrid']")))

                except TimeoutException:
                    to_proceed = False
                    while to_proceed == False:
                        try:
                            while driver.execute_script("return document.readyState;") != "complete":
                                time.sleep(0.5)
                            captcha_to_solve = WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                                (By.XPATH, "//div[@class='blockUI blockMsg blockPage']//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[@src='jcaptchaCustom.jpg' and @border='1']")))
                            captcha_code = solve_captcha(
                                captcha_elem_to_solve=captcha_to_solve, driver=driver)

                            while driver.execute_script("return document.readyState;") != "complete":
                                time.sleep(0.5)
                            captcha_field = WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                                (By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//input[@type='text']")))
                            captcha_field.clear()
                            captcha_field.send_keys(captcha_code)
                            submit_captcha_button = driver.find_element(
                                By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[contains(@src, 'btnGo')]")
                            a.move_to_element(
                                submit_captcha_button).click().perform()

                            try:
                                while driver.execute_script("return document.readyState;") != "complete":
                                    time.sleep(0.5)
                                WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                                    (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))

                            except TimeoutException:
                                to_proceed = True
                                # break

                        except TimeoutException:
                            current_input_row = CurrentInputRow.get_instance()
                            current_row_id = current_input_row.get_id(
                                self=current_input_row)
                            data_id_range = DataIdRange.get_instance()
                            data_id_end = data_id_range.get_end_id(
                                self=data_id_range)
                            self.finding_coverage(
                                driver, a, data_id_start=current_row_id, data_id_end=data_id_end)
                            raise Exception(
                                "Error in the SEARCHING step of coverage_check.py - table did not pop up after clicking 'Search'. Captcha did not pop up too.")
                    while driver.execute_script("return document.readyState;") != "complete":
                        time.sleep(0.5)
                    WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                        (By.XPATH, "//table[@id='resultAddressGrid']")))

                number_of_results = len(driver.find_elements(
                    By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"))

                if number_of_results == 0:
                    number_of_results = len(driver.find_elements(
                        By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"))

                if number_of_results > 50:
                    if lot_no_detail_flag == 0:
                        unit_no_filter_tab = driver.find_element(
                            By.XPATH, "//input[@id='flt0_resultAddressGrid' and @type='text' and @class='flt']")
                        unit_no_filter_tab.clear()
                        current_input_row = CurrentInputRow.get_instance()
                        unit_no_filter_tab.send_keys(current_input_row.get_house_unit_lotno(
                            self=current_input_row).strip())
                        self.iterate_through_all_and_notify(
                            driver=driver, a=a, filtered=True, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
                        continue

                    else:
                        # need to search using the lot number too, and look at the number of results.
                        # iterate_through_and_notify() might not work for cases where we need a lot number match.

                        current_row_lot_no = current_input_row.get_house_unit_lotno(
                            self=current_input_row)
                        if len(current_row_lot_no) == 0:
                            # the lot_number of the current row is not defined.
                            raise Exception(
                                f"Error in the iterate_and_notify() step of coverage_check.py - the address with id {current_row_id} does not have a lot number - Yet, we were told to match the lot number.")

                        else:
                            # search using the lot number. iterate and output best match.

                            # we filter the lot number in the table filter row.
                            unit_no_filter_tab = driver.find_element(
                                By.XPATH, "//input[@id='flt0_resultAddressGrid' and @type='text' and @class='flt']")
                            unit_no_filter_tab.clear()
                            current_input_row = CurrentInputRow.get_instance()
                            unit_no_filter_tab.send_keys(current_input_row.get_house_unit_lotno(
                                self=current_input_row).strip())

                            # print("END BLOCK! OUTPUT CASE 3 OR 1 PLEASE!")
                            self.iterate_through_all_and_notify(
                                driver=driver, a=a, filtered=True, lot_no_detail_flag=1, building_name_found=False, street_name_found=True)
                            continue

                elif number_of_results == 0:
                    # no results on the table.
                    write_or_edit_result(
                        id=current_row_id, result_type=8, result_text="No results.")
                    go_back_to_coverage_search_page(driver, a)
                    continue

                else:
                    # the block where 1 < num_of_results < 50
                    if lot_no_detail_flag == 0:
                        (driver, a) = self.search_using_street_type_and_name(
                            driver=driver, a=a)

                        self.iterate_through_all_and_notify(
                            driver, a, filtered=False, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
                        continue

                    else:
                        # when we need to match the lot number.
                        current_row_lot_no = current_input_row.get_house_unit_lotno(
                            self=current_input_row)
                        if len(current_row_lot_no) == 0:
                            # the lot_number of the current row is not defined.
                            raise Exception(
                                f"Error in the iterate_and_notify() step of coverage_check.py - the address with id {current_row_id} does not have a lot number - Yet, we were told to match the lot number.")

                        else:
                            keyword_search_string = current_row_lot_no + ' ' + keyword_search_string

                            keyword_field = driver.find_element(
                                By.XPATH, "//form[@name='Netui_Form_3']//input[@type='text' and contains(@name, 'searchString')]")
                            keyword_field.clear()
                            keyword_field.send_keys(keyword_search_string)

                            # print("END BLOCK! OUTPUT CASE 3 OR 1 PLEASE!")
                            self.iterate_through_all_and_notify(
                                driver=driver, a=a, filtered=False, lot_no_detail_flag=1, building_name_found=False, street_name_found=True)
                            continue
