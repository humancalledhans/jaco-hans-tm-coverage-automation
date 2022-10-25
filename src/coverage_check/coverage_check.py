from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from src.operations.try_diff_xpath_for_results_table import try_diff_xpath_for_results_table
from src.operations.replace_keywords import replace_keywords
from src.operations.filter_unit_num import filter_unit_num
from src.operations.wait_for_results_table import wait_for_results_table
from src.operations.detect_and_solve_captcha import detect_and_solve_captcha, detect_and_solve_captcha_but_rerun
from src.operations.pause_until_loaded import pause_until_loaded
from src.operations.click_search_btn import click_search_btn
from src.singleton.num_of_iterations import NumOfIterations
from src.singleton.cvg_task import CVGTask
from src.singleton.data_id_range import DataIdRange

from src.operations.set_accepted_params import set_accepted_params

from .return_points_for_row import return_points_for_row
from .go_back_to_search_page import go_back_to_coverage_search_page
from .check_coverage_and_notify import check_coverage_and_notify
from .input_speed_requested import input_speed_requested
from src.singleton.current_input_row import CurrentInputRow
from src.singleton.all_the_data import AllTheData
from src.db_read_write.db_write_address import write_or_edit_result
from src.db_read_write.db_read_address import read_from_db


class FindingCoverage:

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

        # search_btn_third_col = driver.find_element(
        #     By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
        # a.move_to_element(search_btn_third_col).click().perform()
        (driver, a) = click_search_btn(driver=driver, a=a)

        # solve captcha

        try:
            (driver, a) = pause_until_loaded(driver, a)
            (driver, a) = wait_for_results_table(driver, a)

        except TimeoutException:
            (driver, a) = detect_and_solve_captcha_but_rerun(driver, a, self)

            (driver, a) = pause_until_loaded(driver, a)

            (driver, a) = wait_for_results_table(driver, a)

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
            if (len(driver.find_elements(By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"))) == 1:
                # for when there's only one result.
                check_coverage_and_notify(
                    table_row_num=0, driver=driver, a=a, filtered=filtered)
                checked = True
                return

            x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']"

        else:
            x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]"

        if len(driver.find_elements(By.XPATH, x_code_path)) == 0 and street_name_found == False and building_name_found == False:
            write_or_edit_result(
                id=current_row_id, result_type=8, result_text="No results.")
            go_back_to_coverage_search_page(driver, a)
            return

        if len(driver.find_elements(By.XPATH, x_code_path)) == 0 and building_name_found == True:
            write_or_edit_result(id=current_row_id, result_type=2,
                                 result_text="Building Name Found, Lot No Not Found.")
            go_back_to_coverage_search_page(driver, a)
            return

        if len(driver.find_elements(By.XPATH, x_code_path)) == 0 and street_name_found == True:
            write_or_edit_result(id=current_row_id, result_type=3,
                                 result_text="Street Name Found, Lot No Not Found.")
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
                    (driver, a) = pause_until_loaded(driver, a)
                    (driver, a) = wait_for_results_table(driver, a)
                    on_page = True
                except TimeoutException:
                    # maybe captcha is here. Let's try to solve it.
                    (driver, a) = detect_and_solve_captcha(driver, a)

            if len(table_header_data) == 0:
                # to assemble the header of the results table.
                datagrid_header = driver.find_elements(
                    By.XPATH, "//tr[@class='datagrid-header']//th[@class='datagrid']")
                for tab in datagrid_header:
                    if tab.text != '':
                        table_header_data.append(tab.text)

            # actually comparing the data of each row.
            table_row_data_list = driver.find_elements(
                By.XPATH, f"({x_code_path})[{table_row_num+1}]//td[@class='datagrid']")

            table_row_data = []
            for table_data in table_row_data_list:
                table_row_data.append(table_data.text)
            (points, lotNumAndStreetAndPostcodeNoMatchBool) = return_points_for_row(
                table_row_data=table_row_data, table_header_data=table_header_data)

            # print("POINTS: ", points, "TABLEROW_NUM: ", table_row_num)
            # if the boolean value is 1, we NEED to return BEST MATCH.
            # else if the boolean value if 0, we just get the highest points.
            # print("POINTS: ", points)
            # print("LOT NUM AND STREET AND POSTCODE NO MATCH BOOL",
            #   lotNumAndStreetAndPostcodeNoMatchBool)
            if points == 'BEST MATCH':
                points_list = []
                check_coverage_and_notify(
                    table_row_num=table_row_num, driver=driver, a=a, filtered=filtered)
                checked = True
                # it's the best that we can get, so we can just break out of the loop.
                break
            else:
                address_used = ''
                for string in table_row_data:
                    string = string.strip()
                    if string != ' ' and string != '-' and len(string) > 0 and string != 'NIL' and string != 'N/A' and string != 'NA' and string != 'N/A ':
                        address_used += string + ' '

                address_used = address_used.strip()
                points_list.append(
                    (table_row_num, points, lotNumAndStreetAndPostcodeNoMatchBool))

        # now, there's no best match. so we take the row with the highest points.
        if checked == False:
            points_list = sorted(points_list, key=lambda x: x[1])

            max_point_tuple = points_list[0]

            if lot_no_detail_flag == 0:
                # print("WENT INTO LOT_NO_DETAIL_FLAG == 0")
                # print("LEN_POINTS_LIST", len(points_list))
                if len(points_list) != 0:
                    # this would mean there's not a best match.

                    check_coverage_and_notify(
                        table_row_num=max_point_tuple[0], driver=driver, a=a, filtered=filtered, address_remark=address_used)
                    checked = True
                    # TODO: 15th October: add the address that's searched on.
            elif lot_no_detail_flag == 1:
                # lot_no_detail_flag == 1.
                # print("WENT INTO LOT_NO_DETAIL_FLAG == 1")
                # print("BUILDING_NAME_FOUND", building_name_found)
                # print("STREET_NAME_FOUND", street_name_found)

                # write remarks, and use the address that's used to search.

                # if lot number or street or postcode not the same (assigned respectively):
                if max_point_tuple[2] == False:

                    if building_name_found == True and street_name_found == False:
                        write_or_edit_result(id=current_row_id, result_type=2,
                                             result_text="Building Name Found, Lot No Not Found.", address_remark=address_used)
                        go_back_to_coverage_search_page(driver, a)
                        return
                    elif building_name_found == False and street_name_found == True:
                        write_or_edit_result(id=current_row_id, result_type=3,
                                             result_text="Street Name Found, Lot No Not Found.", address_remark=address_used)
                        go_back_to_coverage_search_page(driver, a)
                        return

                    elif building_name_found == False and street_name_found == False:
                        # we need to match the lot no, but we couldn't. The building name was also not found. So we output "NO MATCH".
                        write_or_edit_result(
                            id=current_row_id, result_type=8, result_text="No results.", address_remark=address_used)
                        go_back_to_coverage_search_page(driver, a)
                        return

                else:
                    points_list = sorted(points_list, key=lambda x: x[1])

                    max_point_tuple = points_list[0]

                    check_coverage_and_notify(
                        table_row_num=max_point_tuple[0], driver=driver, a=a, filtered=filtered, address_remark=address_used)
                    checked = True

    def select_state(self, driver, a, state):
        # TODO: add condition for when there is only 'Wilayah Persekutuan' in the list.
        # if len(driver.find_elements(By.XPATH, "//select[@id='actionForm_state']//option")) == 1:
        # 	a.move_to_element(driver.find_element(By.XPATH, "//a[contains(text(), 'Help new customer')]")).click().perform()

        (driver, a) = detect_and_solve_captcha(driver, a)

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

        (driver, a) = detect_and_solve_captcha(driver, a)

    def finding_coverage(self, driver, a, data_id_start=-1, data_id_end=-1):

        input_speed_requested(driver, a, 50)

        # we've arrived at the coverage page.
        (driver, a) = pause_until_loaded(driver, a)

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

        # puts all the data from the db into AllTheData() singleton object.
        # AllTheData() singleton contains DataObject() instances.

        # while True:
        num_of_iterations_instance = NumOfIterations.get_instance()
        num_of_iterations = num_of_iterations_instance.get_num_of_iterations()

        for _ in range(num_of_iterations):

            all_the_data = AllTheData.get_instance()
            all_the_data.reset_all_data()

            read_from_db()

            data_range = DataIdRange.get_instance()
            data_range_start = data_range.get_start_id(self=data_range)
            data_range_end = data_range.get_end_id(self=data_range)

            for data in all_the_data.get_all_the_data_list():
                # data all read from db. now, we find the coverage for all the data.

                # if data.get_is_active() == 0:
                #     continue

                # hans: reminder that data_id_start and data_id_end are only used when finding_coverage is started again, from where it had error.

                if data_id_start == -1 and data_id_end == -1:
                    if data.get_id() < data_range_start or data.get_id() > data_range_end:
                        continue
                # elif data_id_start == -1 and data_id_end != -1:
                #     if data.get_id() < data_range_start or data.get_id() > data_id_end:
                #         continue
                # elif data_id_start != -1 and data_id_end == -1:
                #     if data.get_id() < data_id_start or data.get_id() > data_range_end:
                #         continue

                else:
                    if data.get_id() < data_id_start or data.get_id() > data_id_end:
                        continue

                # print("CURRENT ID: ", data.get_id())

                # print("DATA_ID", data_id)
                current_input_row = CurrentInputRow.get_instance()
                current_input_row.set_id(
                    self=current_input_row, current_row_id=data.get_id())
                current_input_row.set_state(
                    self=current_input_row, current_row_state=data.get_state())
                current_input_row.set_postcode(
                    self=current_input_row, current_row_postcode=data.get_postcode())
                current_input_row.set_unit_no(self=current_input_row,
                                              current_row_unit_no=data.get_unit_no())
                current_input_row.set_floor(
                    self=current_input_row, current_row_floor=data.get_floor())
                current_input_row.set_building(self=current_input_row,
                                               current_row_building=data.get_building())
                current_input_row.set_street(self=current_input_row,
                                             current_row_street=data.get_street())
                current_input_row.set_section(
                    self=current_input_row, current_row_section=data.get_section())
                current_input_row.set_city(
                    self=current_input_row, current_row_city=data.get_city())
                current_input_row.set_state(
                    self=current_input_row, current_row_state=data.get_state())
                current_input_row.set_postcode(
                    self=current_input_row, current_row_postcode=data.get_postcode())
                current_input_row.set_search_level_flag(
                    self=current_input_row, current_row_search_level_flag=data.get_search_level_flag())
                current_input_row.set_source(
                    self=current_input_row, current_row_source=data.get_source())
                current_input_row.set_source_id(
                    self=current_input_row, current_row_source_id=data.get_source_id())
                current_input_row.set_salesman(
                    self=current_input_row, current_row_salesman=data.get_salesman())
                current_input_row.set_notify_email(
                    self=current_input_row, current_row_notify_email=data.get_notify_email())
                current_input_row.set_notify_mobile(
                    self=current_input_row, current_row_notify_mobile=data.get_notify_mobile())
                current_input_row.set_result_type(
                    self=current_input_row, current_row_result_type=data.get_result_type())
                current_input_row.set_result_remark(
                    self=current_input_row, current_row_result_remark=data.get_result_remark())
                current_input_row.set_is_active(
                    self=current_input_row, current_row_is_active=data.get_is_active())
                current_input_row.set_created_at(
                    self=current_input_row, current_row_created_at=data.get_created_at())
                current_input_row.set_updated_at(
                    self=current_input_row, current_row_updated_at=data.get_updated_at())

                current_row_id = data.get_id()

                # setting the cvg_task data for current address row id.
                cvg_task = CVGTask.get_instance()
                cvg_task.set_current_id_address_being_checked(
                    current_id=current_row_id)
                cvg_task.increment_current_number_of_addresses_checked()

                # STEP ONE: select state.
                state = current_input_row.get_state(
                    self=current_input_row).upper().strip()

                state_selected = False
                while state_selected == False:
                    try:
                        (driver, a) = pause_until_loaded(driver, a)
                        self.select_state(driver, a, state)
                        state_selected = True

                    except NoSuchElementException:
                        try:
                            help_new_customer_link = driver.find_element(
                                By.XPATH, "//div[@class='wlp-bighorn-window-content']//td[@align='right']//a")
                            a.move_to_element(
                                help_new_customer_link).click().perform()
                            (driver, a) = detect_and_solve_captcha(driver, a)
                            input_speed_requested(driver, a, 50)
                            self.select_state(driver, a, state)
                            state_selected = True
                        except NoSuchElementException:
                            help_new_customer_link = driver.find_element(
                                By.XPATH, "//div[@class='wlp-bighorn-window-content']//td[@align='right']//a")
                            a.move_to_element(
                                help_new_customer_link).click().perform()
                            (driver, a) = detect_and_solve_captcha(driver, a)
                            current_input_row = CurrentInputRow.get_instance()
                            current_row_id = current_input_row.get_id(
                                self=current_input_row)
                            data_id_range = DataIdRange.get_instance()
                            data_id_end = data_id_range.get_end_id(
                                self=data_id_range)
                            self.finding_coverage(
                                driver, a, data_id_start=current_row_id, data_id_end=data_id_end)
                            continue

                # if state_selected == False:
                #     help_new_customer_link = driver.find_element(
                #         By.XPATH, "//div[@class='wlp-bighorn-window-content']//td[@align='right']//a")
                #     a.move_to_element(help_new_customer_link).click().perform()
                #     self.finding_coverage(
                #         driver, a)  # we'll just start over again, since we would only take the data rows that have is_active == 1.
                #     continue

                # THIS EXCEPTION is what we mean:
                # selenium.common.exceptions.NoSuchElementException: Message: Could not locate element with visible text: SELANGOR

                # STEP TWO: set up the search string.
                keyword_search_string = ''

                # STEP TWO A: find if there's a building name.

                lot_no_detail_flag = current_input_row.get_search_level_flag(
                    self=current_input_row)

                # for search_level_flag:
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

                    # search_btn_third_col = driver.find_element(
                    # By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
                    # a.move_to_element(search_btn_third_col).click().perform()
                    (driver, a) = click_search_btn(driver, a)

                    (driver, a) = detect_and_solve_captcha(driver, a)

                    # building name is input.

                    # wait for the results table to pop up.
                    try:
                        (driver, a) = pause_until_loaded(driver, a)
                        (driver, a) = wait_for_results_table(driver, a)
                    except TimeoutException:
                        (driver, a) = detect_and_solve_captcha(driver, a)
                    # captcha should be solved now. getting the results...
                    (driver, a) = pause_until_loaded(driver, a)
                    try:
                        (driver, a) = wait_for_results_table(driver, a)

                        (driver, a, number_of_results) = try_diff_xpath_for_results_table(
                            driver, a)

                        if number_of_results > 50:
                            if lot_no_detail_flag == 0:
                                (driver, a) = filter_unit_num(driver, a)
                                # making sure the filtered resutls pop out, before we proceed.
                                try:
                                    WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                                        (By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")))
                                except TimeoutException:
                                    if len(driver.find_elements(By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")) == 0:
                                        (driver, a) = replace_keywords(driver, a)

                                        try:
                                            WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                                                (By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")))
                                        except TimeoutException:
                                            # search_btn_third_col = driver.find_element(
                                            # By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
                                            # a.move_to_element(
                                            # search_btn_third_col).click().perform()

                                            (driver, a) = click_search_btn(
                                                driver, a)

                                            (driver, a) = detect_and_solve_captcha(
                                                driver, a)

                                        # this would be the correct xpath, as we have filtered using the lot number.
                                        number_of_results = len(driver.find_elements(
                                            By.XPATH, "//tr[@class='odd' or @class='even'][not(@style)]"))

                                        if number_of_results == 0:
                                            (driver, a) = self.search_using_street_type_and_name(
                                                driver=driver, a=a)

                                            (driver, a, number_of_results) = try_diff_xpath_for_results_table(
                                                driver, a)
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
                                (driver, a) = filter_unit_num(driver, a)

                                # making sure the filtered resutls pop out, before we proceed.
                                try:
                                    WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                                        (By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")))
                                except TimeoutException:
                                    if len(driver.find_elements(By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")) == 0:
                                        write_or_edit_result(
                                            id=current_row_id, result_type=8, result_text="No results.")
                                        go_back_to_coverage_search_page(
                                            driver, a)
                                        continue
                                    else:
                                        self.iterate_through_all_and_notify(
                                            driver, a, filtered=True, lot_no_detail_flag=1, building_name_found=True, street_name_found=False)
                                        continue

                                # assuming that the number of results have been significantly reduced.
                                # print("END BLOCK! OUTPUT CASE 2 OR 1 PLEASE!")
                                self.iterate_through_all_and_notify(
                                    driver, a, filtered=True, lot_no_detail_flag=1, building_name_found=True, street_name_found=False)
                                continue
                            else:
                                self.iterate_through_all_and_notify(
                                    driver, a, filtered=True, lot_no_detail_flag=1, building_name_found=True, street_name_found=False)

                        elif number_of_results == 0:
                            # no results found. so we'll try with the "condominium" instead of the "kondominium" variation things.

                            (driver, a, number_of_results) = replace_keywords(
                                driver, a)

                            try:
                                WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                                    (By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")))
                            except TimeoutException:
                                (driver, a) = click_search_btn(driver, a)

                                (driver, a) = detect_and_solve_captcha(driver, a)

                            # print(
                            #     "NUMBER_OF_RESULTS_AFTER_REPLACING JLN and KONDOMINIUM", number_of_results)

                            if number_of_results > 0:
                                self.iterate_through_all_and_notify(
                                    driver, a, filtered=False, lot_no_detail_flag=lot_no_detail_flag, building_name_found=True, street_name_found=False)

                            else:
                                # betul betul takde results.
                                # END BLOCK, OUTPUT CASE 8.

                                (driver, a) = self.search_using_street_type_and_name(
                                    driver=driver, a=a)

                                (driver, a, number_of_results) = try_diff_xpath_for_results_table(
                                    driver, a)

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

                    if len(current_row_street) > 3 and 'NA' != current_row_street.upper() and 'N/A' != current_row_street.upper():
                        keyword_search_string = ''
                        keyword_search_string += current_row_street

                    else:
                        keyword_search_string = ''
                        keyword_search_string += current_input_row.get_section(
                            self=current_input_row)

                    keyword_field = driver.find_element(
                        By.XPATH, "//form[@name='Netui_Form_3']//input[@type='text' and contains(@name, 'searchString')]")
                    keyword_field.clear()
                    keyword_field.send_keys(keyword_search_string)

                    # search_btn_third_col = driver.find_element(
                    # By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
                    # a.move_to_element(search_btn_third_col).click().perform()
                    (driver, a) = click_search_btn(driver, a)

                    # print("CLICKED ON SEARCH!")

                    # solve captcha

                    try:
                        (driver, a) = pause_until_loaded(driver, a)
                        (driver, a) = wait_for_results_table(driver, a)

                    except TimeoutException:
                        detect_and_solve_captcha_but_rerun(driver, a, self)
                        (driver, a) = pause_until_loaded(driver, a)
                        (driver, a) = wait_for_results_table(driver, a)

                    (driver, a, number_of_results) = try_diff_xpath_for_results_table(
                        driver, a)

                    if number_of_results > 50:
                        if lot_no_detail_flag == 0:
                            (driver, a) = filter_unit_num(driver, a)

                            self.iterate_through_all_and_notify(
                                driver=driver, a=a, filtered=True, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
                            continue

                        else:
                            # need to search using the lot number too, and l ook at the number of results.
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
                                (driver, a) = filter_unit_num(driver, a)

                                try:
                                    WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                                        (By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")))
                                except TimeoutException:
                                    # search_btn_third_col = driver.find_element(
                                    # By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
                                    # a.move_to_element(
                                    # search_btn_third_col).click().perform()
                                    (driver, a) = click_search_btn(driver, a)

                                    (driver, a) = detect_and_solve_captcha(
                                        driver, a)

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

                        current_row_lot_no = current_input_row.get_house_unit_lotno(
                            self=current_input_row)
                        if len(current_row_lot_no) == 0:
                            if lot_no_detail_flag == 1:
                                # the lot_number of the current row is not defined.
                                # TODO: Write to DB when lot number is not found. 23 october.
                                raise Exception(
                                    f"Error in the iterate_and_notify() step of coverage_check.py - the address with id {current_row_id} does not have a lot number - Yet, we were told to match the lot number.")

                            else:  # lot_no_detail_flag == 0
                                # the lot_number of the current row is not defined.
                                (driver, a) = self.search_using_street_type_and_name(
                                    driver=driver, a=a)
                                self.iterate_through_all_and_notify(
                                    driver, a, filtered=False, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
                                continue

                        else:
                            # lot number is defined.
                            # search using the lot number. iterate and output best match.

                            if number_of_results == 1:
                                check_coverage_and_notify(
                                    table_row_num=0, driver=driver, a=a, filtered=False)
                                continue

                            else:
                                keyword_search_string = current_input_row.get_street(
                                    self=current_input_row).strip()

                                keyword_field = driver.find_element(
                                    By.XPATH, "//form[@name='Netui_Form_3']//input[@type='text' and contains(@name, 'searchString')]")
                                keyword_field.clear()
                                keyword_field.send_keys(keyword_search_string)

                                (driver, a) = filter_unit_num(driver, a)

                                try:
                                    WebDriverWait(driver, 2).until(EC.presence_of_element_located(
                                        (By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")))
                                except TimeoutException:
                                    # search_btn_third_col = driver.find_element(
                                    # By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
                                    # a.move_to_element(
                                    # search_btn_third_col).click().perform()
                                    (driver, a) = click_search_btn(driver, a)

                                    (driver, a) = detect_and_solve_captcha(
                                        driver, a)

                                self.iterate_through_all_and_notify(
                                    driver=driver, a=a, filtered=True, lot_no_detail_flag=lot_no_detail_flag, building_name_found=False, street_name_found=True)
                                continue