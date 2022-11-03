from src.tm_partners.singleton.current_input_row import CurrentInputRow


def return_points_for_row(table_row_data, table_header_data) -> bool:
    """
    could return "CONFIRMED MATCH" for max possible matches, or the number of columns matched.
    """

    current_input_row = CurrentInputRow.get_instance()

    # assembling input_row_data

    input_unit_num_match_bool = current_input_row.get_search_level_flag(
        self=current_input_row)

    input_house_unit_lotno = current_input_row.get_house_unit_lotno(
        self=current_input_row)

    table_house_unit_lotno_index = table_header_data.index(
        'House/Unit/Lot No.')
    table_house_unit_lotno = table_row_data[table_house_unit_lotno_index]

    if input_house_unit_lotno != table_house_unit_lotno and input_unit_num_match_bool == 1:
        return (0, None)

    else:
        input_street = current_input_row.get_street(self=current_input_row)
        input_section = current_input_row.get_section(self=current_input_row)
        input_floor_no = current_input_row.get_floor(self=current_input_row)
        input_building_name = current_input_row.get_building(
            self=current_input_row)
        input_city = current_input_row.get_city(self=current_input_row)
        input_state = current_input_row.get_state(self=current_input_row)
        input_postcode = current_input_row.get_postcode(self=current_input_row)

        table_street_type_index = table_header_data.index('Street Type')
        table_street_name_index = table_header_data.index('Street Name')
        table_section_index = table_header_data.index('Section')
        table_floor_no_index = table_header_data.index('Floor No.')
        table_building_name_index = table_header_data.index('Building Name')
        table_city_index = table_header_data.index('City')
        table_state_index = table_header_data.index('State')
        table_postcode_index = table_header_data.index('Postcode')

        table_street = table_row_data[table_street_type_index] + \
            ' ' + table_row_data[table_street_name_index]
        table_section = table_row_data[table_section_index]
        table_floor_no = table_row_data[table_floor_no_index]
        table_building_name = table_row_data[table_building_name_index]
        table_city = table_row_data[table_city_index]
        table_state = table_row_data[table_state_index]
        table_postcode = table_row_data[table_postcode_index]

        if input_street.strip().upper() != table_street.strip().upper() or input_state.strip().upper() != table_state.strip().upper():
            return (0, None)

        if len(table_postcode) > 0:
            while table_postcode[0] == '0':
                table_postcode = table_postcode[1:]

        # print("\n\n\n************")
        # print("INPUT_LOT_NO", input_house_unit_lotno,
        #       type(input_house_unit_lotno))
        # print("INPUT_STREET", input_street, type(input_street))
        # print("INPUT_SECTION", input_section, type(input_section))
        # print("INPUT_FLOOR_NO", input_floor_no, type(input_floor_no))
        # print("INPUT_BUILDING_NAME", input_building_name,
        #       type(input_building_name))
        # print("INPUT_CITY", input_city, type(input_city))
        # print("INPUT_STATE", input_state, type(input_state))
        # print("INPUT_POSTCODE", input_postcode, type(input_postcode))
        # print()
        # print("TABLE_LOT_NO", table_house_unit_lotno,
        #       type(table_house_unit_lotno))
        # print("TABLE_STREET", table_street, type(table_street))
        # print("TABLE_SECTION", table_section, type(table_section))
        # print("TABLE_FLOOR_NO", table_floor_no, type(table_floor_no))
        # print("TABLE_BUILDING_NAME", table_building_name,
        #       type(table_building_name))
        # print("TABLE_CITY", table_city, type(table_city))
        # print("TABLE_STATE", table_state, type(table_state))
        # print("TABLE_POSTCODE", table_postcode, type(table_postcode))
        # print("************\n\n\n")

        # time.sleep(30)
        accumulated_points = 0
        best_match_bool = False

        # pseudocode:
        # if it's not best match, we calculate the points.
        # any other scenarios where we should get best match, but we don't?

        # need to count the max number of matches for each address.
        max_points = 0

        if table_house_unit_lotno is not None and table_house_unit_lotno != '' and table_house_unit_lotno != '-':
            max_points += 1
        if table_street is not None and table_street != '' and table_street != '-':
            max_points += 1
        if table_section is not None and table_section != '' and table_section != '-':
            max_points += 1
        if table_floor_no is not None and table_floor_no != '' and table_floor_no != '-':
            max_points += 1
        if table_building_name is not None and table_building_name != '' and table_building_name != '-':
            max_points += 1
        if table_city is not None and table_city != '' and table_city != '-':
            max_points += 1
        if table_state is not None and table_state != '' and table_state != '-':
            max_points += 1
        if table_postcode is not None and table_postcode != '' and table_postcode != '-':
            max_points += 1

        # if input_building_name is None and input_house_unit_lotno is not None and input_street is not None and input_section is not None and input_floor_no is not None and input_city is not None and input_state is not None and input_postcode is not None:
        #     if input_house_unit_lotno == table_house_unit_lotno and input_street.strip() == table_street.strip() and input_section.strip() == table_section.strip() and input_city.strip() == table_city.strip() and input_state.strip() == table_state.strip() and input_postcode == table_postcode:
        #         best_match_bool = True
        #         return "BEST MATCH"
        #     else:
        #         best_match_bool = False
        # elif input_building_name is not None and input_floor_no is None and input_house_unit_lotno is not None and input_street is not None and input_section is not None and input_city is not None and input_state is not None and input_postcode is not None:
        #     if input_house_unit_lotno == table_house_unit_lotno and input_street == table_street and input_section == table_section and input_floor_no == table_floor_no and input_building_name == table_building_name and input_city == table_city and input_state == table_state and input_postcode == table_postcode:
        #         best_match_bool = True
        #         return "BEST MATCH"
        #     else:
        #         best_match_bool = False

        # if best_match_bool == False:

        lotNumAndStreetAndPostcodeNoMatchBool = True

        if input_house_unit_lotno is not None and input_house_unit_lotno != '':
            if input_house_unit_lotno == table_house_unit_lotno:
                accumulated_points = accumulated_points + 1
            else:
                lotNumAndStreetAndPostcodeNoMatchBool = False
        if input_street is not None and input_street != '':
            if input_street.upper().strip() == table_street.upper().strip():
                accumulated_points = accumulated_points + 1
            else:
                lotNumAndStreetAndPostcodeNoMatchBool = False
        if input_section is not None and input_section != '':
            if input_section.upper().strip().strip() == table_section.upper().strip().strip():
                accumulated_points = accumulated_points + 1
        if input_floor_no is not None and input_floor_no != '':
            if input_floor_no == table_floor_no:
                accumulated_points = accumulated_points + 1
        if input_building_name is not None and input_building_name != '':
            if input_building_name.upper().strip().strip() == table_building_name.upper().strip().strip():
                accumulated_points = accumulated_points + 1
        if input_city is not None and input_city != '':
            if input_city.upper().strip().strip() == table_city.upper().strip().strip():
                accumulated_points = accumulated_points + 1
        if input_state is not None and input_state != '':
            if input_state.upper().strip().strip() == table_state.upper().strip().strip():
                accumulated_points = accumulated_points + 1
        if input_postcode is not None and input_postcode != '':
            if input_postcode == table_postcode:
                accumulated_points = accumulated_points + 1
            # else:
            #     lotNumAndStreetAndPostcodeNoMatchBool = False

        if accumulated_points == max_points:
            best_match_bool = True
            return ("BEST MATCH", None)

        return (accumulated_points, lotNumAndStreetAndPostcodeNoMatchBool)
