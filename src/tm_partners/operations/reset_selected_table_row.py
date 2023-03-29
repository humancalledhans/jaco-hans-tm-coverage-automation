from src.tm_partners.singleton.selected_table_row import SelectedTableRow


def reset_selected_table_row():

    selected_table_row = SelectedTableRow.get_instance()
    selected_table_row.set_unit_no(selected_table_row, None)
    selected_table_row.set_street_type(selected_table_row, None)
    selected_table_row.set_street_name(selected_table_row, None)
    selected_table_row.set_section(selected_table_row, None)
    selected_table_row.set_floor(selected_table_row, None)
    selected_table_row.set_building(selected_table_row, None)
    selected_table_row.set_city(selected_table_row, None)
    selected_table_row.set_state(selected_table_row, None)
    selected_table_row.set_postcode(selected_table_row, None)
