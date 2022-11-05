import time
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from src.tm_partners.coverage_check.check_coverage_and_notify_actual import check_coverage_and_notify_actual
from src.tm_partners.operations.enter_into_keyword_field import enter_into_keyword_field
from src.tm_partners.operations.waiting_for_results_table import waiting_for_results_table
from src.tm_partners.operations.try_diff_xpath_for_results_table import try_diff_xpath_for_results_table
from src.tm_partners.operations.replace_keywords import replace_keywords
from src.tm_partners.operations.filter_unit_num import filter_unit_num
from src.tm_partners.operations.wait_for_results_table import wait_for_results_table
from src.tm_partners.operations.detect_and_solve_captcha import detect_and_solve_captcha, detect_and_solve_captcha_but_rerun
from src.tm_partners.operations.set_accepted_params import set_accepted_params
from src.tm_partners.operations.go_back_to_search_page import go_back_to_coverage_search_page
from src.tm_partners.operations.select_state import select_state
from src.tm_partners.operations.set_current_db_row import set_current_db_row
from src.tm_partners.operations.search_using_street import search_using_street_type_and_name
from src.tm_partners.operations.pause_until_loaded import pause_until_loaded
from src.tm_partners.operations.click_search_btn import click_search_btn
from src.tm_partners.operations.iterate_through_all_and_notify import iterate_through_all_and_notify

from src.tm_partners.singleton.num_of_iterations import NumOfIterations
from src.tm_partners.singleton.cvg_task import CVGTask
from src.tm_partners.singleton.data_id_range import DataIdRange

from src.tm_partners.singleton.current_db_row import CurrentDBRow
from src.tm_partners.singleton.all_the_data import AllTheData
from src.tm_partners.db_read_write.db_get_largest_id import get_max_id_from_db
from src.tm_partners.db_read_write.db_write_address import write_or_edit_result
from src.tm_partners.db_read_write.db_read_address import read_from_db
from src.tm_partners.coverage_check.bridge_to_actual_op import bridge_to_actual_op

from .check_coverage_and_notify import check_coverage_and_notify
from .input_speed_requested import input_speed_requested


class FindingCoverage:

    def __init__(self):
        pass

    def finding_coverage(self, driver, a, data_id_start=-1, data_id_end=-1):

        input_speed_requested(driver, a, 50)

        (driver, a) = pause_until_loaded(driver, a)

        set_accepted_params()

        num_of_iterations_instance = NumOfIterations.get_instance()
        num_of_iterations = num_of_iterations_instance.get_num_of_iterations()

        data_range = DataIdRange.get_instance()
        data_range_start = data_range.get_start_id(self=data_range)
        data_range_end = data_range.get_end_id(self=data_range)

        for _ in range(num_of_iterations):
            # hans, the loop starts at coverage search page. (the page where you select state and enter keyword)

            all_the_data = AllTheData.get_instance()
            all_the_data.reset_all_data()

            data_id_range = DataIdRange.get_instance()
            data_id_range.set_end_id(
                self=data_id_range, end_id=get_max_id_from_db())

            read_from_db()

            # initialise cvg_task
            cvg_task = CVGTask.get_instance()
            cvg_task.set_total_number_of_addresses_to_check(
                len(all_the_data.get_all_the_data_list()))

            for data in all_the_data.get_all_the_data_list():
                all_the_data = AllTheData.get_instance()
                all_the_data.reset_all_data()

                read_from_db()

                print("CURRENT ID: ", data.get_id())

                if data.get_is_active() == 0:
                    continue

                # hans: reminder that data_id_start and data_id_end are only used when finding_coverage is started again, from where it had error.
                if data_id_start == -1 and data_id_end == -1:
                    if data.get_id() < data_range_start or data.get_id() > data_range_end:
                        continue

                else:
                    if data.get_id() < data_id_start or data.get_id() > data_id_end:
                        continue

                print("CURRENT RUNNING ID: ", data.get_id())

                set_current_db_row(data)

                current_db_row = CurrentDBRow.get_instance()
                current_row_id = current_db_row.get_id(
                    self=current_db_row)

                print("\n", current_db_row.get_address(
                    self=current_db_row))

                # STEP ONE: select state.
                state = current_db_row.get_state(
                    self=current_db_row).upper().strip()

                state_selected = False
                while state_selected == False:
                    try:
                        (driver, a) = pause_until_loaded(driver, a)
                        (driver, a) = select_state(driver, a, state)
                        state_selected = True

                    except NoSuchElementException:
                        try:
                            help_new_customer_link = driver.find_element(
                                By.XPATH, "//div[@class='wlp-bighorn-window-content']//td[@align='right']//a")
                            a.move_to_element(
                                help_new_customer_link).click().perform()
                            (driver, a) = detect_and_solve_captcha(driver, a)
                            input_speed_requested(driver, a, 50)
                            (driver, a) = select_state(driver, a, state)
                            state_selected = True
                        except NoSuchElementException:
                            help_new_customer_link = driver.find_element(
                                By.XPATH, "//div[@class='wlp-bighorn-window-content']//td[@align='right']//a")
                            a.move_to_element(
                                help_new_customer_link).click().perform()
                            (driver, a) = detect_and_solve_captcha(driver, a)
                            current_db_row = CurrentDBRow.get_instance()
                            current_row_id = current_db_row.get_id(
                                self=current_db_row)
                            data_id_range = DataIdRange.get_instance()
                            data_id_end = data_id_range.get_end_id(
                                self=data_id_range)
                            self.finding_coverage(
                                driver, a, data_id_start=current_row_id, data_id_end=data_id_end)
                            continue

                # STEP TWO: set up the search string.
                keyword_search_string = ''

                # STEP TWO A: find if there's a building name.

                lot_no_detail_flag = current_db_row.get_search_level_flag(
                    self=current_db_row)

                # for search_level_flag:
                # 0 means don't need to match lot number.
                # 1 means need to match lot number. Allows for cases like 'Building/Street name found, lot number not found'
                # refer to code in iterate_through_all_and_notify(). block where checked==False

                building_name = current_db_row.get_building(
                    self=current_db_row)

                if building_name is not None:
                    building_name = building_name.strip()

                if building_name != '' and building_name is not None and len(building_name) > 3:

                    # get the building name, and search the results using that query.

                    keyword_search_string = keyword_search_string + building_name

                    (driver, a) = enter_into_keyword_field(
                        driver, a, keyword_search_string)

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
                                    (driver, a) = waiting_for_results_table(
                                        driver, a)
                                except TimeoutException:
                                    if len(driver.find_elements(By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")) == 0:
                                        (driver, a) = replace_keywords(
                                            driver, a, keyword_search_string)

                                        try:
                                            (driver, a) = waiting_for_results_table(
                                                driver, a)
                                        except TimeoutException:

                                            (driver, a) = click_search_btn(
                                                driver, a)

                                            (driver, a) = detect_and_solve_captcha(
                                                driver, a)

                                        # this would be the correct xpath, as we have filtered using the lot number.
                                        number_of_results = len(driver.find_elements(
                                            By.XPATH, "//tr[@class='odd' or @class='even'][not(@style)]"))

                                        if number_of_results == 0:
                                            (driver, a) = search_using_street_type_and_name(self=self,
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
                                                iterate_through_all_and_notify(
                                                    driver, a, filtered=False, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
                                                continue

                                    else:
                                        iterate_through_all_and_notify(
                                            driver, a, filtered=True, lot_no_detail_flag=0, building_name_found=True, street_name_found=False)
                                        continue

                                iterate_through_all_and_notify(
                                    driver, a, filtered=True, lot_no_detail_flag=0, building_name_found=True, street_name_found=False)
                                continue

                            elif lot_no_detail_flag == 1:
                                (driver, a) = filter_unit_num(driver, a)

                                # making sure the filtered resutls pop out, before we proceed.
                                try:
                                    (driver, a) = waiting_for_results_table(
                                        driver, a)
                                except TimeoutException:
                                    if len(driver.find_elements(By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style)]")) == 0:
                                        write_or_edit_result(
                                            id=current_row_id, result_type=8, result_text="No results.")
                                        go_back_to_coverage_search_page(
                                            driver, a)
                                        continue
                                    else:
                                        iterate_through_all_and_notify(
                                            driver, a, filtered=True, lot_no_detail_flag=1, building_name_found=True, street_name_found=False)
                                        continue

                                # assuming that the number of results have been significantly reduced.
                                # print("END BLOCK! OUTPUT CASE 2 OR 1 PLEASE!")
                                iterate_through_all_and_notify(
                                    driver, a, filtered=True, lot_no_detail_flag=1, building_name_found=True, street_name_found=False)
                                continue
                            else:
                                iterate_through_all_and_notify(
                                    driver, a, filtered=True, lot_no_detail_flag=1, building_name_found=True, street_name_found=False)

                        elif number_of_results == 0:
                            # no results found. so we'll try with the "condominium" instead of the "kondominium" variation things.

                            (driver, a, number_of_results) = replace_keywords(
                                driver, a, keyword_search_string)

                            try:
                                (driver, a) = waiting_for_results_table(
                                    driver, a)
                            except TimeoutException:
                                (driver, a) = click_search_btn(driver, a)

                                (driver, a) = detect_and_solve_captcha(
                                    driver, a)

                            # print(
                            #     "NUMBER_OF_RESULTS_AFTER_REPLACING JLN and KONDOMINIUM", number_of_results)

                            if number_of_results > 0:
                                iterate_through_all_and_notify(
                                    driver, a, filtered=False, lot_no_detail_flag=lot_no_detail_flag, building_name_found=True, street_name_found=False)

                            else:
                                # betul betul takde results.
                                # END BLOCK, OUTPUT CASE 8.

                                (driver, a) = self.search_using_street_type_and_name(self=self,
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
                                    iterate_through_all_and_notify(
                                        driver, a, filtered=False, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
                                    continue
                        else:
                            # the block where 1 < num_of_results < 50
                            if lot_no_detail_flag == 0:
                                iterate_through_all_and_notify(
                                    driver, a, filtered=False, lot_no_detail_flag=0, building_name_found=True, street_name_found=False)
                                continue

                            else:
                                # print("END BLOCK! OUTPUT CASE 2 OR 1 PLEASE!")
                                iterate_through_all_and_notify(
                                    driver, a, filtered=False, lot_no_detail_flag=1, building_name_found=True, street_name_found=False)
                                continue
                    except TimeoutException:
                        try:
                            driver.find_element(
                                By.XPATH, "//table[@border='0' and @class='errorDisplay1']//tbody//tr//td//b[contains(text(), 'Sorry, we are unable to proceed at the moment. This error could be due to loss of connection to the server. Please try again later.')]")
                            continue
                        except NoSuchElementException:
                            raise Exception("Results table did not pop up.")
                else:
                    # when building name is empty. do the same but for street.

                    # get street_type_and_search() gets the lot no, street type, and street name - puts it tgt and searches.
                    # the results table would then be there.
                    # then, it calls iterate_through_all_and_notify().

                    current_row_street = current_db_row.get_street(
                        self=current_db_row)

                    if len(current_row_street) > 3 and 'NA' != current_row_street.upper() and 'N/A' != current_row_street.upper():
                        keyword_search_string = ''
                        keyword_search_string += current_row_street

                    else:
                        keyword_search_string = ''
                        keyword_search_string += current_db_row.get_section(
                            self=current_db_row)

                    (driver, a) = enter_into_keyword_field(
                        driver, a, keyword_search_string)

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
                            iterate_through_all_and_notify(
                                driver=driver, a=a, filtered=True, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
                            continue

                        else:
                            # print('lot num detail flag = 1')
                            # need to search using the lot number too, and l ook at the number of results.
                            # iterate_through_and_notify() might not work for cases where we need a lot number match.
                            current_row_lot_no = current_db_row.get_house_unit_lotno(
                                self=current_db_row)
                            if len(current_row_lot_no) == 0:
                                # print(' lot num not defined')
                                # the lot_number of the current row is not defined.
                                raise Exception(
                                    f"Error in the iterate_and_notify() step of coverage_check.py - the address with id {current_row_id} does not have a lot number - Yet, we were told to match the lot number.")

                            else:
                                # print('lot num is defined!!')

                                # search using the lot number. iterate and output best match.

                                # we filter the lot number in the table filter row.
                                (driver, a) = filter_unit_num(driver, a)

                                try:
                                    # print('before waiting for results')
                                    (driver, a) = waiting_for_results_table(
                                        driver, a)
                                    # print('after waiting for results')
                                except TimeoutException:
                                    # search_btn_third_col = driver.find_element(
                                    # By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
                                    # a.move_to_element(
                                    # search_btn_third_col).click().perform()
                                    (driver, a) = click_search_btn(driver, a)

                                    (driver, a) = detect_and_solve_captcha(
                                        driver, a)

                                # print("END BLOCK! OUTPUT CASE 3 OR 1 PLEASE!")
                                # print('before iterate through all and notify')
                                iterate_through_all_and_notify(
                                    driver=driver, a=a, filtered=True, lot_no_detail_flag=1, building_name_found=False, street_name_found=True)
                                # print('after iterate through all and notify')
                                continue

                    elif number_of_results == 0:
                        # no results on the table.

                        write_or_edit_result(
                            id=current_row_id, result_type=8, result_text="No results.")
                        go_back_to_coverage_search_page(driver, a)
                        continue

                    else:
                        # the block where 1 < num_of_results < 50

                        current_row_lot_no = current_db_row.get_house_unit_lotno(
                            self=current_db_row)
                        if len(current_row_lot_no) == 0:
                            if lot_no_detail_flag == 1:
                                # the lot_number of the current row is not defined.
                                # TODO: Write to DB when lot number is not found. 23 october.
                                raise Exception(
                                    f"Error in the iterate_and_notify() step of coverage_check.py - the address with id {current_row_id} does not have a lot number - Yet, we were told to match the lot number.")

                            else:  # lot_no_detail_flag == 0
                                # the lot_number of the current row is not defined.
                                (driver, a) = self.search_using_street_type_and_name(self=self,
                                                                                     driver=driver, a=a)
                                iterate_through_all_and_notify(
                                    driver, a, filtered=False, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
                                continue

                        else:
                            # lot number is defined.
                            # search using the lot number. iterate and output best match.

                            if number_of_results == 1:
                                (driver, a) = check_coverage_and_notify(
                                    table_row_num=0, driver=driver, a=a, filtered=False)
                                (driver, a) = bridge_to_actual_op(driver, a)
                                check_coverage_and_notify_actual(
                                    driver=driver, a=a, address_remark=None, to_notify=False)

                                driver.close()
                                driver.switch_to.window(
                                    driver.window_handles[0])
                                continue

                            else:
                                keyword_search_string = current_db_row.get_street(
                                    self=current_db_row).strip()

                                (driver, a) = enter_into_keyword_field(
                                    driver, a, keyword_search_string)

                                (driver, a) = filter_unit_num(driver, a)

                                try:
                                    (driver, a) = waiting_for_results_table(
                                        driver, a)
                                except TimeoutException:
                                    # search_btn_third_col = driver.find_element(
                                    # By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
                                    # a.move_to_element(
                                    # search_btn_third_col).click().perform()
                                    (driver, a) = click_search_btn(driver, a)

                                    (driver, a) = detect_and_solve_captcha(
                                        driver, a)

                                iterate_through_all_and_notify(
                                    driver=driver, a=a, filtered=True, lot_no_detail_flag=lot_no_detail_flag, building_name_found=False, street_name_found=True)
                                continue
            # except Exception as e:
            #     print('Exception: ', e)
            #     continue
