import time
from src.tm_partners.singleton.current_db_row import CurrentDBRow
from src.tm_partners.coverage_check.check_coverage_and_notify import check_coverage_and_notify
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException

from src.tm_partners.operations.wait_for_results_table import wait_for_results_table
from src.tm_partners.operations.detect_and_solve_captcha import detect_and_solve_captcha

from src.tm_partners.operations.pause_until_loaded import pause_until_loaded
from src.tm_partners.operations.set_selected_table_row import set_selected_table_row
from src.tm_partners.operations.return_points_for_row import return_points_for_row
from src.tm_partners.operations.go_back_to_search_page import go_back_to_coverage_search_page
from src.tm_partners.coverage_check.check_coverage_and_notify import check_coverage_and_notify
from src.tm_partners.db_read_write.db_write_address import write_or_edit_result
from src.tm_partners.operations.possible_multiple_best_match_operation import possible_multiple_best_match_operation
from src.tm_partners.coverage_check.bridge_to_actual_op import bridge_to_actual_op
from src.tm_partners.coverage_check.check_coverage_and_notify_actual import check_coverage_and_notify_actual
from src.tm_partners.coverage_check.input_speed_requested import input_speed_requested
from src.tm_partners.operations.login import Login
from src.tm_partners.singleton.retry_at_end import RetryAtEndCache


def iterate_through_all_and_notify(driver, a, filtered, lot_no_detail_flag, building_name_found, street_name_found):
    """
    this function
    1. gets to the actual results page,
    2. iterates through all the results, and
    3. calculates the points of every results
    4. and calls "check_coverage_and_notify()" with the best result row.

    NOTE: 'building_name_found' means the building name is found in the results page.
    NOTE: the table_row_num starts from 0. that is, 0 is the first row of a result in the result table.
    """
    current_db_row = CurrentDBRow.get_instance()
    current_row_id = current_db_row.get_id(self=current_db_row)

    points_list = []
    best_match_row_num_list = []
    table_header_data = []

    checked = False

    if filtered == False:
        if (len(driver.find_elements(By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"))) == 1:
            # for when there's only one result.
            
            # setting the selected table row
            x_code_path = "//table[@id='resultAddressGrid']//tr[@class='datagrid-odd' or @class='datagrid-even']"
            set_selected_table_row(driver, a, x_code_path, 0)

            (driver, a) = check_coverage_and_notify(
                table_row_num=0, driver=driver, a=a, filtered=False)
            (driver, a) = bridge_to_actual_op(driver, a)
            (current_row_id, result_type, result_text) = check_coverage_and_notify_actual(
                driver=driver, a=a)
            write_or_edit_result(
                id=current_row_id, result_type=result_type, result_text=result_text)

            if result_type != 7:
                driver.close()
                driver.switch_to.window(
                    driver.window_handles[0])
            else:
                retry_at_end_singleton = RetryAtEndCache.get_instance()
                retry_at_end_singleton.add_data_id_to_retry(
                    self=retry_at_end_singleton, data_id=current_db_row.get_id(self=current_db_row))
                time.sleep(7)
                driver.quit()
                login = Login()
                (driver, a) = login.login()
                (driver, a) = input_speed_requested(
                    driver, a, 50)

            checked = True
            return

    x_code_path = "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style='display: none;')]"

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
        (points, lotNumAndStreetAndPostcodeNumMatchBool) = return_points_for_row(
            table_row_data=table_row_data, table_header_data=table_header_data)

        # print("POINTS: ", points, "TABLEROW_NUM: ", table_row_num)
        # if the boolean value is 1, we NEED to return BEST MATCH.
        # else if the boolean value if 0, we just get the highest points.
        # print("POINTS: ", points)
        # print("LOT NUM AND STREET AND POSTCODE NO MATCH BOOL",
        #   lotNumAndStreetAndPostcodeNumMatchBool)

        if points == 'BEST MATCH':
            points_list = []
            best_match_row_num_list.append(table_row_num)

        elif points != 'BEST MATCH' and len(best_match_row_num_list) == 0:
            address_used = ''
            for string in table_row_data:
                string = string.strip()
                if string != ' ' and string != '-' and len(string) > 0 and string != 'NIL' and string != 'N/A' and string != 'NA' and string != 'N/A ':
                    address_used += string + ' '

            address_used = address_used.strip()
            points_list.append(
                (table_row_num, points, lotNumAndStreetAndPostcodeNumMatchBool))
    if len(best_match_row_num_list) > 0:

        # print("BEST MATCH ROW NUM LIST: ", best_match_row_num_list)

        set_selected_table_row(driver, a, x_code_path,
                               best_match_row_num_list[0], 100)

        possible_multiple_best_match_operation(
            driver, a, best_match_row_num_list, filtered)
        checked = True

    # now, there's no best match. so we take the row with the highest points.
    if checked == False:
        points_list = sorted(points_list, key=lambda x: x[1])

        max_point_tuple = points_list[0]

        set_selected_table_row(driver, a, x_code_path,
                               max_point_tuple[0], max_point_tuple[1])

        if lot_no_detail_flag == 0:
            # print("WENT INTO LOT_NO_DETAIL_FLAG == 0")
            # print("LEN_POINTS_LIST", len(points_list))
            if len(points_list) != 0:
                # this would mean there's not a best match.

                (driver, a) = check_coverage_and_notify(
                    table_row_num=max_point_tuple[0], driver=driver, a=a, filtered=False)
                (driver, a) = bridge_to_actual_op(driver, a)
                (current_row_id, result_type, result_text) = check_coverage_and_notify_actual(
                    driver=driver, a=a)
                write_or_edit_result(
                    id=current_row_id, result_type=result_type, result_text=result_text)

                if result_type != 7:
                    driver.close()
                    driver.switch_to.window(
                        driver.window_handles[0])
                else:
                    retry_at_end_singleton = RetryAtEndCache.get_instance()
                    retry_at_end_singleton.add_data_id_to_retry(
                        self=retry_at_end_singleton, data_id=current_db_row.get_id(self=current_db_row))
                    time.sleep(7)
                    driver.quit()
                    login = Login()
                    (driver, a) = login.login()
                    (driver, a) = input_speed_requested(
                        driver, a, 50)

                checked = True
        elif lot_no_detail_flag == 1:

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

                set_selected_table_row(
                    driver, a, x_code_path, max_point_tuple[0], max_point_tuple[1])

                (driver, a) = check_coverage_and_notify(
                    table_row_num=max_point_tuple[0], driver=driver, a=a, filtered=filtered)
                (driver, a) = bridge_to_actual_op(driver, a)
                (current_row_id, result_type, result_text) = check_coverage_and_notify_actual(
                    driver=driver, a=a)
                write_or_edit_result(
                    id=current_row_id, result_type=result_type, result_text=result_text)

                if result_type != 7:
                    driver.close()
                    driver.switch_to.window(
                        driver.window_handles[0])
                else:
                    retry_at_end_singleton = RetryAtEndCache.get_instance()
                    retry_at_end_singleton.add_data_id_to_retry(
                        self=retry_at_end_singleton, data_id=current_db_row.get_id(self=current_db_row))
                    time.sleep(7)
                    driver.quit()
                    login = Login()
                    (driver, a) = login.login()
                    (driver, a) = input_speed_requested(
                        driver, a, 50)

                checked = True
