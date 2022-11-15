from src.tm_global.singleton.selected_table_row import SelectedTableRow
from src.tm_global.singleton.lot_num_match_bool import LotNumMatchBool
from src.tm_global.singleton.current_db_row import CurrentDBRow


def set_lot_num_or_building_name_match_if_appropriate():
    """
    if the best address we got in the website does not match the lot number in the database and lot num match is 1, then we set the lot number match bool to false.
    """
    lot_num_match_bool_singleton = LotNumMatchBool.get_instance()
    lot_num_match_bool = lot_num_match_bool_singleton.get_lotnummatch(
        self=lot_num_match_bool_singleton)

    current_db_row_singleton = CurrentDBRow.get_instance()

    selected_table_row_instance = SelectedTableRow.get_instance()

    part_used_for_address = selected_table_row_instance.get_part_of_address_used(
        self=selected_table_row_instance)

    if lot_num_match_bool and current_db_row_singleton.get_search_level_flag(self=current_db_row_singleton):
        selected_table_row_instance = SelectedTableRow.get_instance()

        selected_table_row_instance.set_result_remark(
            self=selected_table_row_instance, result_remark=f"{part_used_for_address} Found, Lot Number Not Found, and Lot Number match bool = 1.")
