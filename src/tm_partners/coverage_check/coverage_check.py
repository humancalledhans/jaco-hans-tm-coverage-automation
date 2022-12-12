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
from src.tm_partners.operations.filter_unit_num import filter_unit_num
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

from .check_coverage_and_notify import check_coverage_and_notify
from .input_speed_requested import input_speed_requested

class FindingCoverage:

    def __init__(self):
        pass

    def finding_coverage(self, driver, a):
        """Main driver that attains the desired outcome

        Args:
            driver: the selenium driver
            a: ActionChains object
        """
        
        # handling intermediatory page for speed selection
        (driver, a) = input_speed_requested(driver, a, 50)
        (driver, a) = pause_until_loaded(driver, a)

        # setup
        set_accepted_params()

        num_of_iterations_instance = NumOfIterations.get_instance()
        num_of_iterations = num_of_iterations_instance.get_num_of_iterations()

        data_range = DataIdRange.get_instance()
        data_range_start = data_range.get_start_id(self=data_range)
        data_range_end = data_range.get_end_id(self=data_range)

        for _ in range(num_of_iterations):
            all_the_data = AllTheData.get_instance()
            all_the_data.reset_all_data(self=all_the_data)

            read_from_db()

            all_the_data_list = all_the_data.get_all_the_data_list(
                self=all_the_data)

            # initialise cvg_task
            cvg_task = CVGTask.get_instance()
            cvg_task.set_total_number_of_addresses_to_check(len(all_the_data_list))

            for address_to_search in all_the_data_list:
                search_results_agg = []

                set_current_db_row(address_to_search)
                current_db_row = CurrentDBRow.get_instance()
                
                print("Searching coverage for ID:", current_db_row.get_id(self=current_db_row))
                print(current_db_row.get_address(self=current_db_row))

                # Preprocess the input to get all variations by token
                address_keywords_to_search = self._get_address_keywords_to_search(current_db_row)
                
                # TODO: Filter by state & address keyword until result is acceptable
                # Case 1: < 1024
                # Case 2: == 1024
                state_token = current_db_row.get_state(self=current_db_row).upper().strip()

                for address_keyword in address_keywords_to_search:
                    
                    # don't search if the address_keyword is too short
                    if len(address_keyword) < 3:
                        continue

                    # only happens when captcha pops up
                    current_search_success = False
                    while not current_search_success:
                        print("Searching for keyword:", address_keyword)

                        # select state from dropdown
                        (driver, a) = pause_until_loaded(driver, a)
                        (driver, a) = select_state(driver, a, state_token)

                        # enter keyword to search
                        (driver, a) = enter_into_keyword_field(
                        driver, a, address_keyword)
                        (driver, a) = click_search_btn(driver, a)
                        (driver, a, did_captcha_interfere) = detect_and_solve_captcha(driver, a, True)

                        # wait for the results table to pop up.
                        try:
                            (driver, a) = pause_until_loaded(driver, a)
                            (driver, a) = wait_for_results_table(driver, a)
                        except TimeoutException:
                            (driver, a, did_captcha_interfere) = detect_and_solve_captcha(driver, a, True)

                        # redoing the search due to captcha interference
                        if not did_captcha_interfere:
                            current_search_success = True
                        
                        # TODO: use the realtime filtering to narrow down by city and postcode
                        # TODO: store the results in an array
                        table_rows = driver.find_elements(By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even']")
                        for row in table_rows:
                            row_data = []
                            row_cells = row.find_elements(By.TAG_NAME, "td")
                            for cell in row_cells:
                                row_data.append(cell.text)
                            search_results_agg.append({
                                'unit_no': row_data[0],
                                'street': row_data[1] + ' ' + row_data[2],
                                'section': row_data[3],
                                'floor': row_data[4],
                                'building': row_data[5],
                                'city': row_data[6],
                                'state': row_data[7],
                                'postcode': row_data[8],
                            })
                            print(len(search_results_agg))
                        

                # TODO: Find closest match (don't forget flag)
                # TODO: Concatenation to get address result
                # TODO: Check result & store in DB

    def _get_address_keywords_to_search(self, current_db_row:CurrentDBRow):
        
        """Generates address keywords to search

        Args:
            current_db_row: CurrentDBRow object

        Returns:
            [string]: array of strings to search
        """
        address_keywords_to_search = []

        # include tokens that shouldn't have variations
        address_keywords_to_search.extend(
            [
                current_db_row.get_house_unit_lotno(self=current_db_row),
                current_db_row.get_city(self=current_db_row),
                current_db_row.get_postcode(self=current_db_row)
            ]
        )

        # include tokens that might have variations
        building_name_variations = self._get_variations(current_db_row.get_building(self=current_db_row))
        street_name_variations = self._get_variations(current_db_row.get_street(self=current_db_row))
        section_variations = self._get_variations(current_db_row.get_section(self=current_db_row))
        
        address_keywords_to_search = [
            *address_keywords_to_search,
            *building_name_variations, 
            *street_name_variations, 
            *section_variations
        ]
        
        return address_keywords_to_search
        
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
            'APPARTMENT': ['APT', 'APPT'],
            'APT': ['APPARTMENT', 'APPT'],
            'APPT': ['APPARTMENT', 'APT'],
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