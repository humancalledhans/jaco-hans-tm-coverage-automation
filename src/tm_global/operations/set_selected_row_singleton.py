from src.tm_global.assumptions.table_column_headers_assumption import return_assummed_table_column_headers
from src.tm_global.singleton.selected_table_row import SelectedTableRow


def set_selected_row_singleton(all_results_sorted):
    selected_table_row_instance = SelectedTableRow.get_instance()
    selected_table_row_instance.set_is_best_match(
        self=selected_table_row_instance, is_best_match=all_results_sorted[1][0] == 'BEST MATCH')
    # print('set is best match', all_results_sorted[0][1][0] == 'BEST MATCH')

    assummed_table_column_headers = return_assummed_table_column_headers()
    selected_table_row_instance.set_unit_no(
        self=selected_table_row_instance, selected_table_row_unit_no=all_results_sorted[0][0][assummed_table_column_headers.index('House / Unit No')])
    # print('set unit no', all_results_sorted[0][0][0][assummed_table_column_headers.index(
    # 'House / Unit No')])
    selected_table_row_instance.set_street_type(
        self=selected_table_row_instance, selected_table_row_street_type=all_results_sorted[0][0][assummed_table_column_headers.index('Street Type')])
    # print('set street type',
    #   all_results_sorted[0][0][0][assummed_table_column_headers.index('Street Type')])
    selected_table_row_instance.set_street_name(
        self=selected_table_row_instance, selected_table_row_street_name=all_results_sorted[0][0][assummed_table_column_headers.index('Street Name')])
    # print('set street name',
    #   all_results_sorted[0][0][0][assummed_table_column_headers.index('Street Name')])
    selected_table_row_instance.set_section(
        self=selected_table_row_instance, selected_table_row_section=all_results_sorted[0][0][assummed_table_column_headers.index('Section')])
    # print('set section', all_results_sorted[0][0][0]
    #   [assummed_table_column_headers.index('Section')])
    selected_table_row_instance.set_floor(
        self=selected_table_row_instance, selected_table_row_floor=all_results_sorted[0][0][assummed_table_column_headers.index('Floor No')])
    # print('set floor', all_results_sorted[0][0][0]
    #   [assummed_table_column_headers.index('Floor No')])
    selected_table_row_instance.set_building(
        self=selected_table_row_instance, selected_table_row_building=all_results_sorted[0][0][assummed_table_column_headers.index('Building Name')])
    # print('set building', all_results_sorted[0][0][0][assummed_table_column_headers.index(
    # 'Building Name')])
    selected_table_row_instance.set_city(
        self=selected_table_row_instance, selected_table_row_city=all_results_sorted[0][0][assummed_table_column_headers.index('City')])
    # print('set city', all_results_sorted[0][0][0]
    #   [assummed_table_column_headers.index('City')])
    selected_table_row_instance.set_postcode(
        self=selected_table_row_instance, selected_table_row_postcode=all_results_sorted[0][0][assummed_table_column_headers.index('Postcode')])
    # print('set postcode', all_results_sorted[0][0][0]
    #   [assummed_table_column_headers.index('Postcode')])
