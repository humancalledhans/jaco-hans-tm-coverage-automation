import time
from src.tm_global.operations.set_current_db_row_singleton import set_current_db_row_singleton
from src.tm_global.singleton.all_the_data import AllTheData
from src.tm_global.singleton.data_id_range import DataIdRange
from src.tm_global.singleton.num_of_iterations import NumOfIterations
from src.tm_global.singleton.cvg_task import CVGTask
from src.tm_global.db_read_write.db_read_address import read_from_db
from src.tm_global.operations.select_state import select_state
from src.tm_global.operations.enter_into_keyword_field import enter_into_keyword_field
from src.tm_global.operations.set_up_input_keyword import enter_right_keyword
from src.tm_global.operations.return_to_coverage_search_page import return_to_coverage_search_page
from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.filter_by_lot_num import filter_by_lot_number
from src.tm_global.operations.choose_best_from_all_results import choose_best_match_from_all_results


def finding_coverage(driver, a, data_id_start=-1, data_id_end=-1):
    num_of_iterations_instance = NumOfIterations.get_instance()
    num_of_iterations = num_of_iterations_instance.get_num_of_iterations()

    # get range of data to search.
    data_range = DataIdRange.get_instance()
    data_range_start = data_range.get_start_id(self=data_range)
    data_range_end = data_range.get_end_id(self=data_range)

    # initialise cvg_task
    cvg_task = CVGTask.get_instance()
    cvg_task.set_total_number_of_addresses_to_check(
        num_of_iterations * (data_range_end - data_range_start) + 1)

    for _ in range(num_of_iterations):
        all_the_data = AllTheData.get_instance()
        all_the_data.reset_all_data()

        read_from_db()

        for data in all_the_data.get_all_the_data_list():
            print("CURRENT ROW ID: ", data.get_id())
            if data_id_start == -1 and data_id_end == -1:
                if data.get_id() < data_range_start or data.get_id() > data_range_end:
                    continue
            else:
                if data.get_id() < data_id_start or data.get_id() > data_id_end:
                    continue

            set_current_db_row_singleton(data)

            try:
                # select state.
                (driver, a) = select_state(driver, a)

            except Exception as e:
                current_db_row = CurrentDBRow.get_instance()
                print("ERROR ID:", current_db_row.get_id(
                    self=current_db_row))
                print("the select state error")
                time.sleep(30)

            try:
                (driver, a) = enter_right_keyword(driver, a)

            except Exception("No results found using building name, street name, or section name."):
                print(
                    "no results found using building name, street name, or section name.")

            except Exception as e:
                current_db_row = CurrentDBRow.get_instance()
                print("ERROR ID:", current_db_row.get_id(
                    self=current_db_row))
                print('the right keyword error')
                print(e)
                time.sleep(300)
                continue

            finally:
                # TODO: you should probably loop through each, and get marks for all rows.
                # You'll have the lotNumberMatch boolean value. if the lot_no_detail_flag is 1, then sort points with bool value == 1. else, sort only with points.
                # filter using lot number. (if applicable)
                (driver, a) = filter_by_lot_number(driver, a)

                choose_best_match_from_all_results(driver, a)

                # we iterate through all the results and find the best match.
                # (driver, a) = iterate_through_all_results(driver, a)

                # filter_iterate_and_notify(driver, a)

            print("--------------------\n")
            (driver, a) = return_to_coverage_search_page(driver, a)

    return (driver, a)
