from singleton.current_input_row import CurrentInputRow


def return_points_for_row(table_row_data_list, table_header_data) -> bool:
    """
    could return "CONFIRMED MATCH" for max possible matches, or the number of columns matched.
    """
    table_row_data = []
    for table_data in table_row_data_list:
        table_row_data.append(table_data.text)

    current_input_row = CurrentInputRow()

    input_unit_num_match_bool = current_input_row.get_lotno_match_bool()

    input_house_unit_lotno = current_input_row.get_house_unit_lotno()

    table_house_unit_lotno_index = table_header_data.index(
        'House/Unit/Lot No.')
    table_house_unit_lotno = table_row_data[table_house_unit_lotno_index]

    if input_house_unit_lotno != table_house_unit_lotno and input_unit_num_match_bool == 1:
        return 0

    else:
        input_street_type = current_input_row.get_street_type()
        input_street_name = current_input_row.get_street_name()
        input_section = current_input_row.get_section()
        input_floor_no = current_input_row.get_floor_no()
        input_building_name = current_input_row.get_building_name()
        input_city = current_input_row.get_city()
        input_state = current_input_row.get_state()
        input_postcode = current_input_row.get_postcode()

        table_street_type_index = table_header_data.index('Street Type')
        table_street_name_index = table_header_data.index('Street Name')
        table_section_index = table_header_data.index('Section')
        table_floor_no_index = table_header_data.index('Floor No.')
        table_building_name_index = table_header_data.index('Building Name')
        table_city_index = table_header_data.index('City')
        table_state_index = table_header_data.index('State')
        table_postcode_index = table_header_data.index('Postcode')

        table_street_type = table_row_data[table_street_type_index]
        table_street_name = table_row_data[table_street_name_index]
        table_section = table_row_data[table_section_index]
        table_floor_no = table_row_data[table_floor_no_index]
        table_building_name = table_row_data[table_building_name_index]
        table_city = table_row_data[table_city_index]
        table_state = table_row_data[table_state_index]
        table_postcode = table_row_data[table_postcode_index]

        accumulated_points = 0

        # determines the number of columns, that has actual data.
        actual_data_col_counter = 0

        # the block below's the one that's always stuck.

        # this block calculates the maximum number of columns that can be matched.

        if input_house_unit_lotno == table_house_unit_lotno and input_house_unit_lotno != '':
            accumulated_points = accumulated_points + 1
        if input_street_type.upper().strip().strip() == table_street_type.upper().strip().strip() and input_street_type != '':
            accumulated_points = accumulated_points + 1
        if input_street_name.upper().strip().strip() == table_street_name.upper().strip().strip() and input_street_name != '':
            accumulated_points = accumulated_points + 1
        if input_section.upper().strip().strip() == table_section.upper().strip().strip() and input_section != '':
            accumulated_points = accumulated_points + 1
        if input_floor_no == table_floor_no and input_floor_no != '':
            accumulated_points = accumulated_points + 1
        if input_building_name.upper().strip().strip() == table_building_name.upper().strip().strip() and input_building_name != '':
            accumulated_points = accumulated_points + 1
        if input_city.upper().strip().strip() == table_city.upper().strip().strip() and input_city != '':
            accumulated_points = accumulated_points + 1
        if input_state.upper().strip().strip() == table_state.upper().strip().strip() and input_state != '':
            accumulated_points = accumulated_points + 1
        if input_postcode == table_postcode and input_postcode != '':
            accumulated_points = accumulated_points + 1

        if accumulated_points == actual_data_col_counter:
            return "BEST MATCH"
        else:
            return accumulated_points
