from src.tm_global.singleton.selected_table_row import SelectedTableRow
from src.tm_global.singleton.current_db_row import CurrentDBRow


def reset_singleton_values_for_next_address():
    selected_table_row_instance = SelectedTableRow.get_instance()
    selected_table_row_instance.reset_all_values(
        self=selected_table_row_instance)

    current_db_row_instance = CurrentDBRow.get_instance()
    current_db_row_instance.reset_all_values(self=current_db_row_instance)
