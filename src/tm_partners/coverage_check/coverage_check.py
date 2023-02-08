import time
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from src.tm_partners.coverage_check.check_coverage_and_notify_actual import check_coverage_and_notify_actual
from src.tm_partners.operations.enter_into_keyword_field import enter_into_keyword_field
from src.tm_partners.operations.waiting_for_results_table import waiting_for_results_table
from src.tm_partners.operations.try_diff_xpath_for_results_table import try_diff_xpath_for_results_table
from src.tm_partners.operations.replace_keywords import replace_keywords
from src.tm_partners.operations.filter_unit_num import filter_unit_num, reset_unit_num_filter
from src.tm_partners.operations.wait_for_results_table import wait_for_results_table
from src.tm_partners.operations.detect_and_solve_captcha import detect_and_solve_captcha
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
from src.tm_partners.singleton.retry_at_end import RetryAtEndCache
from src.tm_partners.operations.login import Login
from src.tm_partners.coverage_check.reset_singletons import reset_singletons
from src.tm_partners.operations.filter_city import filter_city
from src.tm_partners.operations.filter_section import filter_section
from src.tm_partners.operations.filter_street import filter_street

from .check_coverage_and_notify import check_coverage_and_notify
from .input_speed_requested import input_speed_requested


class FindingCoverage:

    def __init__(self):
        pass

    def finding_coverage(self, driver, a):

        (driver, a) = input_speed_requested(driver, a, 50)

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
            all_the_data.reset_all_data(self=all_the_data)
            read_from_db()
            all_the_data_list = all_the_data.get_all_the_data_list(
                self=all_the_data)

            # initialise cvg_task
            cvg_task = CVGTask.get_instance()
            cvg_task.set_total_number_of_addresses_to_check(self=cvg_task, 
                total_number_of_addresses_to_check=len(all_the_data_list))

            for data in all_the_data_list:

                try:

                    print("CURRENT ID: ", data.get_id())

                    # if data.get_is_active() == 0:
                    #     continue

                    # hans: reminder that rebooted_start_id and rebooted_end_id are only used when finding_coverage is started again, from where it had error.
                    if data.get_id() < data_range_start or data.get_id() > data_range_end:
                        continue

                    print("CURRENT RUNNING ID: ", data.get_id())

                    reset_singletons()
                    set_current_db_row(data)

                    current_db_row = CurrentDBRow.get_instance()
                    current_row_id = current_db_row.get_id(
                        self=current_db_row)

                    print("\n", current_db_row.get_address_with_headers(
                        self=current_db_row))

                    # STEP ONE: select state.
                    self._select_state(driver, a, data)

                    # STEP TWO: set up the search string.
                    # keyword_search_string = ''

                    # NOTE
                    # for search_level_flag:
                    # 0 means don't need to match lot number.
                    # 1 means need to match lot number. Allows for cases like 'Building/Street name found, lot number not found'
                    # refer to code in iterate_through_all_and_notify(). block where checked==False
                    
                    # STEP TWO A: find if there's a building name.
                    building_name = current_db_row.get_building(
                        self=current_db_row)

                    if building_name is not None:
                        building_name = building_name.strip()

                    is_building_name_exists = building_name is not None and len(building_name) > 3
                    if is_building_name_exists:
                        self._search_for_building_match(driver, a, building_name)
                        continue

                    # STEP TWO B: find if there's a street/section name.
                    # when building name is empty. do the same but for street, or for section name.
                    street_name = current_db_row.get_street(
                        self=current_db_row)
                    section_name = current_db_row.get_section(
                            self=current_db_row)
                    
                    if street_name is not None:
                        street_name = street_name.strip()
                    if section_name is not None:
                        section_name = section_name.strip()

                    is_street_name_exists = street_name is not None and len(street_name) > 3
                    is_section_name_exists = section_name is not None and len(section_name) > 2
                    if is_street_name_exists:
                        keyword_search_string = street_name
                    elif is_section_name_exists:
                        keyword_search_string = section_name
                    else:
                        self._write_no_result()
                        continue
                        
                    self._search_for_street_or_section_match(driver, a, keyword_search_string)

                except Exception as e:
                    try:
                        WebDriverWait(driver, 1).until(EC.presence_of_element_located(
                            (By.XPATH, "//div[@class='blockUI blockMsg blockPage']//div[@class='subContent']//b[contains(text(), 'Your session has expired due to inactivity.')]")))
                        driver.find_element(
                            By.XPATH, "//div[@class='blockUI blockMsg blockPage']//div[@class='subContent']//b[contains(text(), 'Your session has expired due to inactivity.')]")
                        dismiss_btn = driver.find_element(
                            By.XPATH, "//div[@class='blockUI blockMsg blockPage']//input[@type='button' and @id='timeout_ok']")
                        a.move_to_element(dismiss_btn).click().perform()
                        (driver, a) = pause_until_loaded(driver, a)
                        driver.quit()
                        login = Login()
                        (driver, a) = login.login()
                        (driver, a) = input_speed_requested(
                            driver, a, 50)
                        continue
                    except NoSuchElementException:
                        print('Exception: ', e)
                        retry_at_end_singleton = RetryAtEndCache.get_instance()
                        retry_at_end_singleton.add_data_id_to_retry(
                            self=retry_at_end_singleton, data_id=data.get_id())
                        time.sleep(7)
                        driver.quit()
                        login = Login()
                        (driver, a) = login.login()
                        (driver, a) = input_speed_requested(
                            driver, a, 50)
                        continue
                    except:
                        print('Exception: ', e)
                        retry_at_end_singleton = RetryAtEndCache.get_instance()
                        retry_at_end_singleton.add_data_id_to_retry(
                            self=retry_at_end_singleton, data_id=data.get_id())
                        time.sleep(7)
                        driver.quit()
                        login = Login()
                        (driver, a) = login.login()
                        (driver, a) = input_speed_requested(
                            driver, a, 50)

    def _select_state(self, driver, a, data):
        """Picks the relevant state from the dropdown
        Args:
            driver: selenium driver
            a: ActionChains object
            data: address data to process
        """
        current_db_row = CurrentDBRow.get_instance()

        state = current_db_row.get_state(
            self=current_db_row).upper().strip()

        state_selected = False
        while state_selected == False:
            try:
                (driver, a) = pause_until_loaded(driver, a)
                (driver, a) = select_state(driver, a, state)
                state_selected = True

            except NoSuchElementException:  # exception is caused by select_stat
                try:
                    print('select state select budao')
                    help_new_customer_link = WebDriverWait(driver, 1).until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='wlp-bighorn-window-content']//td[@align='right']//a")))
                    a.move_to_element(
                        help_new_customer_link).click().perform()
                    try:
                        (driver, a) = detect_and_solve_captcha(
                            driver, a)
                        (driver, a) = input_speed_requested(
                            driver, a, 50)
                        (driver, a) = select_state(
                            driver, a, state)
                        state_selected = True
                    except NoSuchElementException:
                        (driver, a) = detect_and_solve_captcha(
                            driver, a)

                        retry_at_end_singleton = RetryAtEndCache.get_instance()
                        retry_at_end_singleton.add_data_id_to_retry(
                            self=retry_at_end_singleton, data_id=data.get_id())
                        time.sleep(7)
                        driver.quit()
                        login = Login()
                        (driver, a) = login.login()
                        (driver, a) = input_speed_requested(
                            driver, a, 50)
                        continue
                    except:
                        print('Exception: ', e)
                        retry_at_end_singleton = RetryAtEndCache.get_instance()
                        retry_at_end_singleton.add_data_id_to_retry(
                            self=retry_at_end_singleton, data_id=data.get_id())
                        time.sleep(7)
                        driver.quit()
                        login = Login()
                        (driver, a) = login.login()
                        (driver, a) = input_speed_requested(
                            driver, a, 50)
                        continue

                except TimeoutException:
                    (driver, a) = detect_and_solve_captcha(driver, a)

                    retry_at_end_singleton = RetryAtEndCache.get_instance()
                    retry_at_end_singleton.add_data_id_to_retry(
                        self=retry_at_end_singleton, data_id=data.get_id())
                    time.sleep(7)
                    driver.quit()
                    login = Login()
                    (driver, a) = login.login()
                    (driver, a) = input_speed_requested(driver, a, 50)
                    continue

            except TimeoutException:
                (driver, a) = detect_and_solve_captcha(driver, a)

                retry_at_end_singleton = RetryAtEndCache.get_instance()
                retry_at_end_singleton.add_data_id_to_retry(
                    self=retry_at_end_singleton, data_id=data.get_id())
                time.sleep(7)
                driver.quit()
                login = Login()
                (driver, a) = login.login()
                (driver, a) = input_speed_requested(driver, a, 50)
                continue

    def _search_for_building_match(self, driver, a, building_name):
        """Searching for the best result using building name. No result 
        will be recorded if a match is not found.
        Args:
            driver: selenium driver
            a: ActionChains object
            building_name (str): a valid building name
        Raises:
            Exception: when result table doesn't show
        """
        
        current_db_row = CurrentDBRow.get_instance()
        lot_no_detail_flag = current_db_row.get_search_level_flag(
                        self=current_db_row)
        

        _, building_name_variations = self._preprocess_building_name(building_name)
        keyword_search_string = None

        # finding good keyword to use (that returns decent num of results)
        for building_name_variation in building_name_variations:
            try:
                # building name is input.
                (driver, a) = enter_into_keyword_field(
                    driver, a, building_name_variation)

                (driver, a) = click_search_btn(driver, a)

                (driver, a) = detect_and_solve_captcha(driver, a)

                # wait for the results table to pop up.
                try:
                    (driver, a) = pause_until_loaded(driver, a)
                    (driver, a) = wait_for_results_table(driver, a)
                except TimeoutException:
                    (driver, a) = detect_and_solve_captcha(driver, a)
            except NoSuchElementException:
                print('retry keywords 5')
                time.sleep(7)
                retry_at_end_singleton = RetryAtEndCache.get_instance()
                retry_at_end_singleton.add_data_id_to_retry(
                    self=retry_at_end_singleton, data_id=current_db_row.get_id(self=current_db_row))
                time.sleep(7)
                driver.quit()
                login = Login()
                (driver, a) = login.login()
                (driver, a) = input_speed_requested(
                    driver, a, 50)
                return
            except:
                print('retry keywords 5')
                time.sleep(7)
                retry_at_end_singleton = RetryAtEndCache.get_instance()
                retry_at_end_singleton.add_data_id_to_retry(
                    self=retry_at_end_singleton, data_id=current_db_row.get_id(self=current_db_row))
                time.sleep(7)
                driver.quit()
                login = Login()
                (driver, a) = login.login()
                (driver, a) = input_speed_requested(
                    driver, a, 50)
                return        
            
            # checking if the number of results is acceptable
            number_of_results = len(driver.find_elements(
                By.XPATH, "//tr[@class='odd' or @class='even' or @class='datagrid-odd' or @class='datagrid-even'][not(@style)]"))
            if number_of_results == 1024 and keyword_search_string is None:
                keyword_search_string = building_name_variation
            elif 0 < number_of_results < 1024:
                keyword_search_string = building_name_variation
                break
        
        # handle when building turns no results
        if keyword_search_string is None:
            self._write_no_result()
            return
        # edge case when number of results reached 1024 then 0 upon keyword re-search
        elif number_of_results == 0:
            # building name is input.
            (driver, a) = enter_into_keyword_field(
                driver, a, keyword_search_string)

            (driver, a) = click_search_btn(driver, a)

            (driver, a) = detect_and_solve_captcha(driver, a)

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

            # too many results
            if number_of_results > 50:
                # using the filters
                (driver, a) = filter_street(driver, a)
                (driver, a) = filter_section(driver, a)
                (driver, a) = filter_city(driver, a)

                # IDEA: If flag is 0, try to filter by unit and evaluate the results.
                # If no results, remove the unit filter and evaluate.
                if lot_no_detail_flag == 0:
                    (driver, a) = filter_unit_num(driver, a)
                    
                    # making sure the filtered resutls pop out, before we proceed.
                    # NOTE: in this try/except block, we are setting the correct x_code_path, because it can be diff due to filtering applied
                    try:
                        (driver, a) = waiting_for_results_table(
                            driver, a)
                        x_code_path = "//tr[@class='odd' or @class='even'][not(@style)]"
                    
                    except TimeoutException:
                        x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style='display: none;')]"
                        if len(driver.find_elements(By.XPATH, x_code_path)) == 0:
                            try:
                                # this would be the correct xpath, as we have filtered using the lot number.
                                number_of_results = len(driver.find_elements(
                                    By.XPATH, "//tr[@class='odd' or @class='even'][not(@style)]"))

                                if number_of_results == 0:
                                    # clear the unit filter
                                    (driver, a) = reset_unit_num_filter(driver, a)

                            except NoSuchElementException:
                                print('retry keywords 1')
                                time.sleep(7)
                                retry_at_end_singleton = RetryAtEndCache.get_instance()
                                retry_at_end_singleton.add_data_id_to_retry(
                                    self=retry_at_end_singleton, data_id=current_db_row.get_id(self=current_db_row))
                                time.sleep(7)
                                driver.quit()
                                login = Login()
                                (driver, a) = login.login()
                                (driver, a) = input_speed_requested(
                                    driver, a, 50)
                                return
                        
                    number_of_results = len(driver.find_elements(
                        By.XPATH, x_code_path))

                    if number_of_results == 0:
                        # clear the unit filter
                        (driver, a) = reset_unit_num_filter(driver, a)

                    iterate_through_all_and_notify(
                        driver, a, filtered=True, lot_no_detail_flag=0, building_name_found=True, street_name_found=False)
                    return

                # IDEA: If flag is 1, filter by unit and evaluate the results.
                # If no results, mark "No results" as the outcome
                elif lot_no_detail_flag == 1:
                    (driver, a) = filter_unit_num(driver, a)

                    # making sure the filtered resutls pop out, before we proceed.
                    try:
                        (driver, a) = waiting_for_results_table(
                            driver, a)
                    except TimeoutException:
                    
                        x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style='display: none;')]" 
                        if len(driver.find_elements(By.XPATH, x_code_path)) == 0:
                            self._write_no_result()
                            return  

                    # assuming that the number of results have been significantly reduced
                    iterate_through_all_and_notify(
                        driver, a, filtered=True, lot_no_detail_flag=1, building_name_found=True, street_name_found=False)
                    return
                
            # no results
            # elif number_of_results == 0:
            #     # no results found. so we'll try with the "condominium" instead of the "kondominium" variation things.
            #     try:
            #         (driver, a) = replace_keywords(
            #             driver, a, keyword_search_string)

            #         try:
            #             (driver, a) = waiting_for_results_table(
            #                 driver, a)
            #         except TimeoutException:
            #             (driver, a) = click_search_btn(
            #                 driver, a)

            #             (driver, a) = detect_and_solve_captcha(
            #                 driver, a)

            #         # print(
            #         #     "NUMBER_OF_RESULTS_AFTER_REPLACING JLN and KONDOMINIUM", number_of_results)

            #         if number_of_results > 0:
            #             iterate_through_all_and_notify(
            #                 driver, a, filtered=False, lot_no_detail_flag=lot_no_detail_flag, building_name_found=True, street_name_found=False)

            #         else:
            #             # betul betul takde results.
            #             # END BLOCK, OUTPUT CASE 8.

            #             try:
            #                 (driver, a) = search_using_street_type_and_name(
            #                     driver=driver, a=a)

            #                 (driver, a, number_of_results) = try_diff_xpath_for_results_table(
            #                     driver, a)

            #                 if number_of_results == 0:
            #                     write_or_edit_result(
            #                         id=current_row_id, result_type=8, result_text="No results.")
            #                     go_back_to_coverage_search_page(
            #                         driver, a)
            #                     return

            #                 else:
            #                     iterate_through_all_and_notify(
            #                         driver, a, filtered=False, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
            #                     return
            #                     # (exception from search_using_street_type_and_name)
            #             except TimeoutException:
            #                 retry_at_end_singleton = RetryAtEndCache.get_instance()
            #                 retry_at_end_singleton.add_data_id_to_retry(
            #                     self=retry_at_end_singleton, data_id=current_db_row.get_id(self=current_db_row))
            #                 time.sleep(7)
            #                 driver.quit()
            #                 login = Login()
            #                 (driver, a) = login.login()
            #                 (driver, a) = input_speed_requested(
            #                     driver, a, 50)
            #                 return
            #             except NoSuchElementException:
            #                 print('retry keywords 2')
            #                 time.sleep(5000)
            #                 retry_at_end_singleton = RetryAtEndCache.get_instance()
            #                 retry_at_end_singleton.add_data_id_to_retry(
            #                     self=retry_at_end_singleton, data_id=current_db_row.get_id(self=current_db_row))
            #                 time.sleep(7)
            #                 driver.quit()
            #                 login = Login()
            #                 (driver, a) = login.login()
            #                 (driver, a) = input_speed_requested(
            #                     driver, a, 50)
            #                 return
            #     except NoSuchElementException:
                    print('retry keywords 3')
                    time.sleep(5000)
                    retry_at_end_singleton = RetryAtEndCache.get_instance()
                    retry_at_end_singleton.add_data_id_to_retry(
                        self=retry_at_end_singleton, data_id=current_db_row.get_id(self=current_db_row))
                    time.sleep(7)
                    driver.quit()
                    login = Login()
                    (driver, a) = login.login()
                    (driver, a) = input_speed_requested(
                        driver, a, 50)
                    return
            
            # 1 <= num_of_results < 50
            else:
                if lot_no_detail_flag == 0:
                    iterate_through_all_and_notify(
                        driver, a, filtered=False, lot_no_detail_flag=0, building_name_found=True, street_name_found=False)
                    return

                else:
                    iterate_through_all_and_notify(
                        driver, a, filtered=False, lot_no_detail_flag=1, building_name_found=True, street_name_found=False)
                    return
        
        except TimeoutException:
            try:
                driver.find_element(
                    By.XPATH, "//table[@border='0' and @class='errorDisplay1']//tbody//tr//td//b[contains(text(), 'Sorry, we are unable to proceed at the moment. This error could be due to loss of connection to the server. Please try again later.')]")
                retry_at_end_singleton = RetryAtEndCache.get_instance()
                retry_at_end_singleton.add_data_id_to_retry(
                    self=retry_at_end_singleton, data_id=current_db_row.get_id(self=current_db_row))
                time.sleep(7)
                driver.quit()
                login = Login()
                (driver, a) = login.login()
                (driver, a) = input_speed_requested(
                    driver, a, 50)
                return
            except NoSuchElementException:
                raise Exception(
                    "Results table did not pop up.")

    def _preprocess_building_name(self, building_name: str):
        """Preprocessing the building name by cleaning and generating possible variations
        Args:
            building_name (str): the building name from the DB
        Returns:
            str, [str]: a tuple with the clean name and name variations 
        """ 

        cleaned_building_name = building_name
        building_name_variations = []

        # clean the building name
        terms_to_remove = ['FTTH', 'PPR']
        for term in terms_to_remove:
            cleaned_building_name = cleaned_building_name.replace(term, '')
        cleaned_building_name = cleaned_building_name.strip()

        # find name variations
        building_name_variations = []
        if cleaned_building_name != building_name:
            building_name_variations.append(building_name)
        building_name_variations.extend(self._get_variations(cleaned_building_name))

        return cleaned_building_name, building_name_variations
    
    def _preprocess_street_section_name(self, street_sec_name: str):
        """Preprocessing the street or section name by cleaning and generating possible variations
        Args:
            street_sec_name (str): the building name from the DB
        Returns:
            str, [str]: a tuple with the clean name and name variations 
        """ 

        cleaned_name = street_sec_name.strip()
        name_variations = []

        # find name variations
        name_variations = self._get_variations(cleaned_name)

        return cleaned_name, name_variations

    def _get_variations(self, token:str):
        """Generates possible variations of an address token
        Args:
            token (string): address token
        Returns:
            [string]: an array of token variations, empty if token is ''
        """
        # map of words and all their possible variations as a list
        variation_map = {
            'COMMERCIAL': ['KOMERSIAL'],
            'RESIDENCY': ['RESIDENSI'],
            'TOWER': ['MENARA'],
            'COMPLEX': ['KOMPLEKS'],
            'BAGIAN': ['BHG'],
            'BUKIT': ['BKT'],
            'JABATAN': ['JAB'],
            'JALAN': ['JLN'],
            'KAWASAN': ['KAW'],
            'KEMENTERIAN': ['KEM'],
            'LADANG': ['LDG'],
            'LEMBAGA': ['LEM'],
            'LORONG': ['LRG'],
            'PADANG': ['PDG'],
            'PERSIARAN': ['PSN'],
            'SUNGAI': ['SG'],
            'SIMPANG': ['SPG'],
            'TANJUNG': ['TG'],
            'TELUK': ['TK'],
            'TAMAN': ['TMN'],
            'JALAN': ['JLN'],
            'KOMERSIAL': ['COMMERCIAL'],
            'RESIDENSI': ['RESIDENCY'],
            'MENARA': ['TOWER'],
            'KOMPLEKS': ['COMPLEX'],
            'BHG': ['BAGIAN'],
            'BKT': ['BUKIT'],
            'JAB': ['JABATAN'],
            'JLN': ['JALAN'],
            'KAW': ['KAWASAN'],
            'KEM': ['KEMENTERIAN'],
            'LDG': ['LADANG'],
            'LEM': ['LEMBAGA'],
            'LRG': ['LORONG'],
            'PDG': ['PADANG'],
            'PSN': ['PERSIARAN'],
            'SG': ['SUNGAI'],
            'SPG': ['SIMPANG'],
            'TG': ['TANJUNG'],
            'TK': ['TELUK'],
            'TMN': ['TAMAN'],
            'JLN': ['JALAN'],
            'BLOCK': ['BLOK', 'BLK'],
            'BLOK': ['BLOCK', 'BLK'],
            'BLK': ['BLOCK', 'BLOK'],
            'APARTMENT': ['APT', 'APPT'],
            'APT': ['APARTMENT', 'APPT'],
            'APPT': ['APARTMENT', 'APT'],
            'KAMPUNG': ['KAMPONG', 'KG'],
            'KAMPONG': ['KAMPUNG', 'KG'],
            'KG': ['KAMPUNG', 'KAMPONG'],
            'LEBOH': ['LEBUH', 'LBH'],
            'LEBUH': ['LEBOH', 'LBH'],
            'LBH': ['LEBOH', 'LEBUH'],
            'CONDOMINIUM': ['KONDO', 'CONDO', 'KONDOMINIUM'],
            'KONDO': ['CONDOMINIUM', 'CONDO', 'KONDOMINIUM'],
            'CONDO': ['CONDOMINIUM', 'KONDO', 'KONDOMINIUM'],
            'KONDOMINIUM': ['CONDOMINIUM', 'CONDO', 'KONDO'],
        }

        # token doesn't exist
        if not token:
            return []

        # generate string with variations
        possible_variations = [token]
        token_list = token.split(' ')
        # processing each word in the token
        for i, word in enumerate(token_list):
            # if a variation exists
            if word in variation_map:
                # freeze the state before modification to avoid duplicates
                possible_variations_state_before_mod = [s for s in possible_variations]
                for variation in variation_map[word]:
                    # modify each existing search keyword to include the newly identified variation
                    for possibilities in possible_variations_state_before_mod:
                        new_keyword = possibilities.split(' ')
                        new_keyword[i] = variation
                        possible_variations.append(' '.join(new_keyword)) # list -> string

        return possible_variations

    def _write_no_result(self):
        current_db_row = CurrentDBRow.get_instance()
        current_row_id = current_db_row.get_id(
            self=current_db_row)

        write_or_edit_result(
            id=current_row_id, result_type=8, result_text="No results.")

    def _search_for_street_or_section_match(self, driver, a, street_or_section_name):
        """Searching for the best result using street pr section name. No result 
        will be recorded if a match is not found.
        Args:
            driver: selenium driver
            a: ActionChains object
            building_name (str): a valid street or section name
        """
        
        # get street_type_and_search() gets the lot no, street type, and street name - puts it tgt and searches.
        # the results table would then be there.
        # then, it calls iterate_through_all_and_notify().
        
        keyword_search_string = street_or_section_name
        current_db_row = CurrentDBRow.get_instance()
        lot_no_detail_flag = current_db_row.get_search_level_flag(
            self=current_db_row)

        _, keyword_variations = self._preprocess_street_section_name(keyword_search_string)
        keyword_search_string = None

        # finding good keyword to use (that returns decent num of results)
        for keyword_variation in keyword_variations:
            try:
                # street or section is input.
                (driver, a) = enter_into_keyword_field(
                    driver, a, keyword_variation)

                (driver, a) = click_search_btn(driver, a)

                (driver, a) = detect_and_solve_captcha(driver, a)

                # wait for the results table to pop up.
                try:
                    (driver, a) = pause_until_loaded(driver, a)
                    (driver, a) = wait_for_results_table(driver, a)
                except TimeoutException:
                    (driver, a) = detect_and_solve_captcha(driver, a)
            except NoSuchElementException:
                print('retry keywords 5')
                time.sleep(7)
                retry_at_end_singleton = RetryAtEndCache.get_instance()
                retry_at_end_singleton.add_data_id_to_retry(
                    self=retry_at_end_singleton, data_id=current_db_row.get_id(self=current_db_row))
                time.sleep(7)
                driver.quit()
                login = Login()
                (driver, a) = login.login()
                (driver, a) = input_speed_requested(
                    driver, a, 50)
                return        
            
            # checking if the number of results is acceptable
            number_of_results = len(driver.find_elements(
                By.XPATH, "//tr[@class='odd' or @class='even' or @class='datagrid-odd' or @class='datagrid-even'][not(@style)]"))
            if number_of_results == 1024 and keyword_search_string is None:
                keyword_search_string = keyword_variation
            elif 0 < number_of_results < 1024:
                keyword_search_string = keyword_variation
                break
        
        # handle when street or section turns no results
        if keyword_search_string is None:
            self._write_no_result()
            return
        # edge case when number of results reached 1024 then 0 upon keyword re-search
        elif number_of_results == 0:
            (driver, a) = enter_into_keyword_field(
                driver, a, keyword_search_string)

            (driver, a) = click_search_btn(driver, a)

            # wait for the results table to pop up.
            try:
                (driver, a) = pause_until_loaded(driver, a)
                (driver, a) = wait_for_results_table(driver, a)
            except TimeoutException:
                (driver, a) = detect_and_solve_captcha(driver, a)
            # captcha should be solved now. getting the results...
            (driver, a) = pause_until_loaded(driver, a)

        (driver, a) = wait_for_results_table(driver, a)
        (driver, a, number_of_results) = try_diff_xpath_for_results_table(
            driver, a)

        # too many results
        if number_of_results > 50:

            # IDEA: If flag is 0, try to filter by unit and evaluate the results.
            # If no results, remove the unit filter and evaluate.
            if lot_no_detail_flag == 0:
                (driver, a) = filter_unit_num(driver, a)
                
                # making sure the filtered resutls pop out, before we proceed.
                # NOTE: in this try/except block, we are setting the correct x_code_path, because it can be diff due to filtering applied
                try:
                    (driver, a) = waiting_for_results_table(
                        driver, a)
                    x_code_path = "//tr[@class='odd' or @class='even'][not(@style)]"
                
                except TimeoutException:
                    x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style='display: none;')]"
                    if len(driver.find_elements(By.XPATH, x_code_path)) == 0:
                        try:
                            # this would be the correct xpath, as we have filtered using the lot number.
                            number_of_results = len(driver.find_elements(
                                By.XPATH, "//tr[@class='odd' or @class='even'][not(@style)]"))

                            if number_of_results == 0:
                                # clear the unit filter
                                (driver, a) = reset_unit_num_filter(driver, a)

                        except NoSuchElementException:
                            print('retry keywords 1')
                            time.sleep(7)
                            retry_at_end_singleton = RetryAtEndCache.get_instance()
                            retry_at_end_singleton.add_data_id_to_retry(
                                self=retry_at_end_singleton, data_id=current_db_row.get_id(self=current_db_row))
                            time.sleep(7)
                            driver.quit()
                            login = Login()
                            (driver, a) = login.login()
                            (driver, a) = input_speed_requested(
                                driver, a, 50)
                            return
                    
                number_of_results = len(driver.find_elements(
                    By.XPATH, x_code_path))

                if number_of_results == 0:
                    # clear the unit filter
                    (driver, a) = reset_unit_num_filter(driver, a)

                iterate_through_all_and_notify(
                    driver, a, filtered=True, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
                return

            # IDEA: If flag is 1, filter by unit and evaluate the results.
            # If no results, mark "No results" as the outcome
            elif lot_no_detail_flag == 1:
                (driver, a) = filter_unit_num(driver, a)

                # making sure the filtered resutls pop out, before we proceed.
                try:
                    (driver, a) = waiting_for_results_table(
                        driver, a)
                except TimeoutException:
                
                    x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style='display: none;')]" 
                    if len(driver.find_elements(By.XPATH, x_code_path)) == 0:
                        self._write_no_result()
                        return  

                # assuming that the number of results have been significantly reduced
                iterate_through_all_and_notify(
                    driver, a, filtered=True, lot_no_detail_flag=1, building_name_found=False, street_name_found=True)
                return
            
            
        # 1 <= num_of_results < 50
        else:
            if lot_no_detail_flag == 0:
                iterate_through_all_and_notify(
                    driver, a, filtered=False, lot_no_detail_flag=0, building_name_found=False, street_name_found=True)
                return

            else:
                iterate_through_all_and_notify(
                    driver, a, filtered=False, lot_no_detail_flag=1, building_name_found=False, street_name_found=True)
                return