import re
import time
from selenium.webdriver.common.by import By

from src.tm_global.operations.concatenate_results_from_all_pages import concatenate_results_from_all_pages
from src.tm_global.operations.calculate_points_for_each_row import calculate_points_for_each_row
from src.tm_global.operations.clicked_on_the_right_address import clicked_on_the_right_address


def choose_best_match_from_all_results(driver, a):
    all_results = concatenate_results_from_all_pages(driver, a)
    # return best match row number.
    # tuple: (row_number, points, lotNumAndStreetAndPostcodeNoMatchBool)
    for result_idx in range(len(all_results)):
        # need to determine the column headers first, to match.
        # then, for each row, match the data with those in current_input_row.
        all_results[result_idx] = (all_results[result_idx], calculate_points_for_each_row(
            driver, a, all_results[result_idx]))

    all_results_sorted = []
    results_to_be_removed = []
    print("all_results", all_results)
    for results_idx in range(len(all_results)):
        print('pionts', all_results[results_idx][1][0])
        if all_results[results_idx][1][0] == 'BEST MATCH':
            all_results_sorted.append(all_results[results_idx])
            results_to_be_removed.append(all_results[results_idx])

    for result in results_to_be_removed:
        all_results.remove(result)

    all_results_sorted += sorted(all_results, key=lambda x: x[1][0])
    print("all_results_sorted", all_results_sorted)

    current_page_num = driver.find_element(
        By.XPATH, "//span//a[@class='paginate_button current']").text

    if current_page_num != 1:
        (driver, a) = clicked_on_the_right_address(
            driver, a, all_results_sorted[0])
