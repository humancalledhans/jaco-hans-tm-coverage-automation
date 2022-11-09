from src.tm_partners.coverage_check.check_coverage_and_notify import check_coverage_and_notify
from src.tm_partners.coverage_check.bridge_to_actual_op import bridge_to_actual_op
from src.tm_partners.coverage_check.check_coverage_and_notify_actual import check_coverage_and_notify_actual

from src.tm_partners.db_read_write.db_write_address import write_or_edit_result


def possible_multiple_best_match_operation(driver, a, best_match_row_num_list, filtered):
    best_match_results_list = []
    for row_num in best_match_row_num_list:
        (driver, a) = check_coverage_and_notify(
            row_num, driver, a, filtered)
        (driver, a) = bridge_to_actual_op(driver, a)
        tuple_to_append = check_coverage_and_notify_actual(
            driver, a, to_notify=False)
        best_match_results_list.append(tuple_to_append)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    if len(best_match_results_list) == 1:
        write_or_edit_result(
            id=best_match_results_list[0][0], result_type=best_match_results_list[0][1], result_text=best_match_results_list[0][2])
    else:
        matched_index = -1
        is_case_one_bool = False
        for result in best_match_results_list:
            if result[1] == 1:
                is_case_one_bool = True
                matched_index = result[0]
                break

        if is_case_one_bool and matched_index != -1:
            write_or_edit_result(
                id=matched_index, result_type=1, result_text="Is within serviceable area!")

        else:
            write_or_edit_result(
                id=best_match_results_list[0][0], result_type=best_match_results_list[0][1], result_text=best_match_results_list[0][2])
