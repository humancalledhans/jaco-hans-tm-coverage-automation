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

            if data_range_start != data_range_end:
                data_id_range = DataIdRange.get_instance()
                data_id_range.set_end_id(
                    self=data_id_range, end_id=get_max_id_from_db())

            read_from_db()

            all_the_data_list = all_the_data.get_all_the_data_list(
                self=all_the_data)

            # initialise cvg_task
            cvg_task = CVGTask.get_instance()
            cvg_task.set_total_number_of_addresses_to_check(len(all_the_data_list))

            for input_address in all_the_data_list:
                all_the_data = AllTheData.get_instance()
                all_the_data.reset_all_data(self=all_the_data)

                read_from_db()

                print("CURRENT ID: ", input_address.get_id())