from src.tm_global.singleton.selected_table_row import SelectedTableRow
from src.tm_global.singleton.current_db_row import CurrentDBRow


def write_results_to_db():
    current_db_row = CurrentDBRow.get_instance()
    selected_table_row_instance = SelectedTableRow.get_instance()
    address_used_to_search = selected_table_row_instance.get_address(
        self=selected_table_row_instance)
    print("address used to search: ", address_used_to_search)
    print('database addresss: ', current_db_row.get_address(self=current_db_row))
    print("results for this address:", selected_table_row_instance.get_result_remark(
        self=selected_table_row_instance))

    print("\n* * * * * * * * * * * *\n")
