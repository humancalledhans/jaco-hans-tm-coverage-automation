import time
from src.tm_global.operations.concatenate_results_from_all_pages import concatenate_results_from_all_pages
from src.tm_global.operations.calculate_points_for_each_row import calculate_points_for_each_row
from src.tm_global.operations.clicked_on_the_right_address import coverage_search_the_right_address
from src.tm_global.singleton.lot_num_match_bool import LotNumMatchBool
from src.tm_global.operations.set_selected_row_singleton import set_selected_row_singleton
from src.tm_global.operations.reoptimise_all_results_sorted import reoptimise_all_results_sorted


def choose_best_match_from_all_results(driver, a):
    """
    we only call clicked_on_the_right_address() if there are multiple pages.
    if we have only one page, we can just use the row number.
    """
    all_results = concatenate_results_from_all_pages(driver, a)
    # return best match row number.
    # tuple: (row_number, points, lotNumAndStreetAndPostcodeNoMatchBool)
    print('lengh of all_results: ', len(all_results))
    for result_idx in range(len(all_results)):
        # need to determine the column headers first, to match.
        # then, for each row, match the data with those in current_db_row.
        all_results[result_idx] = (all_results[result_idx], calculate_points_for_each_row(
            driver, a, all_results[result_idx]))

    all_results_sorted = []
    results_to_be_removed = []
    for results_idx in range(len(all_results)):
        if all_results[results_idx][1][0] == 'BEST MATCH':
            all_results_sorted.append(all_results[results_idx])
            results_to_be_removed.append(all_results[results_idx])
            lot_num_match_bool_singleton = LotNumMatchBool.get_instance()
            lot_num_match_bool_singleton.set_lotnummatch(
                self=lot_num_match_bool_singleton, lotnummatch=True)

    # removing the addresses with 'best match', because we added all of them into
    # so that we can have a list with best matches at the front, and highest points appended at the back.
    for result in results_to_be_removed:
        all_results.remove(result)

    all_results_sorted += sorted(all_results, key=lambda x: x[1][0])

    if len(all_results_sorted) > 1:
        if all_results_sorted[0][1][0] != 'BEST MATCH':
            all_results_sorted = reoptimise_all_results_sorted(
                all_results_sorted)

    set_selected_row_singleton(all_results_sorted[0])

    (driver, a) = coverage_search_the_right_address(
        driver, a, all_results_sorted[0])
