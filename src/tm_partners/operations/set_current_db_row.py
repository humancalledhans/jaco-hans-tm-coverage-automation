from src.tm_partners.singleton.current_db_row import CurrentDBRow


def set_current_db_row(data):
    current_db_row = CurrentDBRow.get_instance()
    current_db_row.set_id(
        self=current_db_row, current_row_id=data.get_id())
    current_db_row.set_state(
        self=current_db_row, current_row_state=data.get_state())
    current_db_row.set_postcode(
        self=current_db_row, current_row_postcode=data.get_postcode())
    current_db_row.set_unit_no(self=current_db_row,
                               current_row_unit_no=data.get_unit_no())
    current_db_row.set_floor(
        self=current_db_row, current_row_floor=data.get_floor())
    current_db_row.set_building(self=current_db_row,
                                current_row_building=data.get_building())
    current_db_row.set_street(self=current_db_row,
                              current_row_street=data.get_street())
    current_db_row.set_section(
        self=current_db_row, current_row_section=data.get_section())
    current_db_row.set_city(
        self=current_db_row, current_row_city=data.get_city())
    current_db_row.set_state(
        self=current_db_row, current_row_state=data.get_state())
    current_db_row.set_postcode(
        self=current_db_row, current_row_postcode=data.get_postcode())
    current_db_row.set_search_level_flag(
        self=current_db_row, current_row_search_level_flag=data.get_search_level_flag())
    current_db_row.set_source(
        self=current_db_row, current_row_source=data.get_source())
    current_db_row.set_source_id(
        self=current_db_row, current_row_source_id=data.get_source_id())
    current_db_row.set_salesman(
        self=current_db_row, current_row_salesman=data.get_salesman())
    current_db_row.set_notify_email(
        self=current_db_row, current_row_notify_email=data.get_notify_email())
    current_db_row.set_notify_mobile(
        self=current_db_row, current_row_notify_mobile=data.get_notify_mobile())
    current_db_row.set_result_type(
        self=current_db_row, current_row_result_type=data.get_result_type())
    current_db_row.set_result_remark(
        self=current_db_row, current_row_result_remark=data.get_result_remark())
    current_db_row.set_is_active(
        self=current_db_row, current_row_is_active=data.get_is_active())
    current_db_row.set_created_at(
        self=current_db_row, current_row_created_at=data.get_created_at())
    current_db_row.set_updated_at(
        self=current_db_row, current_row_updated_at=data.get_updated_at())
