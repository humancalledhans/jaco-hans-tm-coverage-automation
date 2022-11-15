from src.tm_global.singleton.selected_table_row import SelectedTableRow


def set_building_or_street_section_name_found_lotno_not_found():

    selected_table_row_instance = SelectedTableRow.get_instance()
    part_of_address_used = selected_table_row_instance.get_part_of_address_used(
        self=selected_table_row_instance)
    selected_table_row_instance.set_result_remark(
        self=selected_table_row_instance, result_remark=f"{part_of_address_used} Found, but Lot Num not Found.")
