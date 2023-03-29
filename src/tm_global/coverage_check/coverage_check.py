import time
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

from src.tm_global.operations.driver_setup import tm_global_driver_setup
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.operations.set_current_db_row_singleton import (
    set_current_db_row_singleton,
)
from src.tm_global.singleton.all_the_data import AllTheData
from src.tm_global.singleton.data_id_range import DataIdRange
from src.tm_global.singleton.num_of_iterations import NumOfIterations
from src.tm_global.singleton.cvg_task import CVGTask
from src.tm_global.db_read_write.db_read_address import read_from_db
from src.tm_global.operations.select_state import select_state
from src.tm_global.operations.set_up_input_keyword import enter_right_keyword
from src.tm_global.operations.return_to_coverage_search_page import (
    return_to_coverage_search_page,
)
from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.filter_by_lot_num import filter_by_lot_number
from src.tm_global.operations.choose_best_from_all_results import (
    choose_best_match_from_all_results,
)
from src.tm_global.singleton.retry_at_end import RetryAtEndCache
from src.tm_global.db_read_write.write_results_to_db import write_results_to_db
from src.tm_global.operations.filter_by_street_name import filter_by_street_name
from src.tm_global.operations.filter_by_building_name import filter_by_building_name
from src.tm_global.operations.filter_by_section_name import filter_by_section_name
from src.tm_global.operations.filter_by_city_name import filter_by_city_name
from src.tm_global.operations.filter_by_postcode import filter_by_postcode
from src.tm_global.operations.reset_singleton_values_for_next_address import (
    reset_singleton_values_for_next_address,
)
from src.tm_global.singleton.selected_table_row import SelectedTableRow
from src.tm_global.singleton.lot_num_match_bool import LotNumMatchBool
from src.tm_global.operations.set_lot_num_or_building_name_match_if_appropriate import (
    set_lot_num_or_building_name_match_if_appropriate,
)
from src.tm_global.operations.search_the_exact_db_address import (
    try_to_search_the_full_address,
)


def finding_coverage(driver, a):

    num_of_iterations_instance = NumOfIterations.get_instance()
    num_of_iterations = num_of_iterations_instance.get_num_of_iterations()

    # for _ in range(num_of_iterations):
    while True:
        all_the_data = AllTheData.get_instance()
        all_the_data.reset_all_data(self=all_the_data)

        read_from_db()

        # get range of data to search.
        data_range = DataIdRange.get_instance()
        data_range_start = data_range.get_start_id(self=data_range)
        data_range_end = data_range.get_end_id(self=data_range)

        # initialise cvg_task
        cvg_task = CVGTask.get_instance()
        cvg_task.set_total_number_of_addresses_to_check(
            num_of_iterations * (data_range_end - data_range_start) + 1
        )

        for data in all_the_data.get_all_the_data_list(self=all_the_data):
            print("CURRENT ROW ID: ", data.get_id())
            # driver should be at https://wholesalepremium.tm.com.my/install/search/address
            if data.get_id() < data_range_start or data.get_id() > data_range_end:
                continue
            reset_singleton_values_for_next_address()
            set_current_db_row_singleton(data)

            try:
                # select state.
                (driver, a) = select_state(driver, a)

            except Exception as e:
                # current_db_row = CurrentDBRow.get_instance()
                # print("ERROR ID:", current_db_row.get_id(
                # self=current_db_row))
                # print("error at select state page (enter address page)")
                retry_at_end_singleton = RetryAtEndCache.get_instance()
                retry_at_end_singleton.add_data_id_to_retry(
                    self=retry_at_end_singleton, data_id=data.get_id()
                )
                (driver, a) = return_to_coverage_search_page(driver, a)
                continue

            try:
                enter_right_keyword_res = enter_right_keyword(driver, a)
                if enter_right_keyword_res != "No results found.":
                    (driver, a) = enter_right_keyword_res

                else:
                    print("No results found.")
                    selected_table_row_instance = SelectedTableRow.get_instance()
                    selected_table_row_instance.set_result_remark(
                        self=selected_table_row_instance,
                        result_remark="No results found.",
                    )
                    (driver, a) = return_to_coverage_search_page(driver, a)
                    # https://wholesalepremium.tm.com.my/coverage-search/result
                    continue

            except NoSuchElementException:
                print("unable to find keyword field")
                # time.sleep(5000)

            try:
                (driver, a) = filter_by_lot_number(driver, a)
                (driver, a) = filter_by_building_name(driver, a)
                (driver, a) = filter_by_street_name(driver, a)
                (driver, a) = filter_by_section_name(driver, a)
                (driver, a) = filter_by_city_name(driver, a)
                (driver, a) = filter_by_postcode(driver, a)
            except Exception:
                # print("error at some excepion her/? by lot number page")
                # # setup driver again.
                # driver = tm_global_driver_setup()
                # driver.get(
                #     'https://wholesalepremium.tm.com.my/install/search/address')
                # a = ActionChains(driver)
                # (driver, a) = pause_until_loaded(driver, a)
                retry_at_end_singleton = RetryAtEndCache.get_instance()
                retry_at_end_singleton.add_data_id_to_retry(
                    self=retry_at_end_singleton, data_id=data.get_id()
                )
                time.sleep(7)
                (driver, a) = return_to_coverage_search_page(driver, a)
                continue

            # except Exception as e:
            #     current_db_row = CurrentDBRow.get_instance()
            #     print("ERROR ID:", current_db_row.get_id(
            #         self=current_db_row))
            #     print(e)
            #     print('the right keyword error. rebooting from id ', current_db_row.get_id(
            #         self=current_db_row))
            #     # driver = tm_global_driver_setup()
            #     # driver.get(
            #     #     'https://wholesalepremium.tm.com.my/install/search/address')
            #     # a = ActionChains(driver)
            #     # (driver, a) = pause_until_loaded(driver, a)
            #     # finding_coverage(
            #     #     driver, a, rebooted_start_id=data_range.get_start_id(self=data_range), rebooted_end_id=data.get_id())
            #     retry_at_end_singleton = RetryAtEndCache.get_instance()
            #     retry_at_end_singleton.add_data_id_to_retry(
            #         self=retry_at_end_singleton, data_id=data.get_id())
            #     time.sleep(7)
            #     continue

            # TODO: you should probably loop through each, and get marks for all rows.
            # You'll have the lotNumberMatch boolean value. if the lot_no_detail_flag is 1, then sort points with bool value == 1. else, sort only with points.
            # filter using lot number. (if applicable)

            # we iterate through all the results and find the best match.
            # (driver, a) = iterate_through_all_results(driver, a)

            # filter_iterate_and_notify(driver, a)
            set_lot_num_or_building_name_match_if_appropriate()
            choose_best_match_from_all_results(driver, a)

            write_results_to_db()
            (driver, a) = return_to_coverage_search_page(driver, a)
