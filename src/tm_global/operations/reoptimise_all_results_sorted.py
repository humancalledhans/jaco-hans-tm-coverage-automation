from src.tm_global.singleton.current_db_row import CurrentDBRow


def reoptimise_all_results_sorted(all_results_sorted):
    """
    only gets the results that are equal to or higher than the number of points that we have, as the highest.
    """
    max_points = all_results_sorted[0][1][0]
    current_db_row = CurrentDBRow.get_instance()
    current_db_row_unit_no = current_db_row.get_house_unit_lotno(
        self=current_db_row)
    for i in range(len(all_results_sorted)):
        if all_results_sorted[i][1][0] < max_points:
            break
        else:
            current_table_row_unit_num = all_results_sorted[i][0][0][0]
            if '-' in current_table_row_unit_num:
                current_table_row_unit_num_split_list = current_table_row_unit_num.split(
                    '-')
                for j in range(len(current_table_row_unit_num_split_list)):
                    if current_table_row_unit_num_split_list[j] in current_db_row_unit_no:
                        new_point = all_results_sorted[i][1][0] + 1
                        previous_bool = all_results_sorted[i][1][1]
                        new_tuple = (
                            all_results_sorted[i][0], (new_point, previous_bool))
                        all_results_sorted[i] = new_tuple

                        continue

            elif current_table_row_unit_num in current_db_row_unit_no:
                new_point = all_results_sorted[i][1][0] + 1
                previous_bool = all_results_sorted[i][1][1]
                new_tuple = (
                    all_results_sorted[i][0], (new_point, previous_bool))
                all_results_sorted[i] = new_tuple

    all_results_sorted_reoptimised = sorted(
        all_results_sorted, key=lambda x: x[1][0], reverse=True)

    return all_results_sorted_reoptimised
