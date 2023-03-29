from src.tm_partners.singleton.current_db_row import CurrentDBRow


def reset_current_db_row():
    current_db_row = CurrentDBRow.get_instance()
    current_db_row.set_id(
        self=current_db_row, current_row_id=None)
    current_db_row.set_state(
        self=current_db_row, current_row_state=None)
    current_db_row.set_postcode(
        self=current_db_row, current_row_postcode=None)
    current_db_row.set_unit_no(self=current_db_row,
                               current_row_unit_no=None)
    current_db_row.set_floor(
        self=current_db_row, current_row_floor=None)
    current_db_row.set_building(self=current_db_row,
                                current_row_building=None)
    current_db_row.set_street(self=current_db_row,
                              current_row_street=None)
    current_db_row.set_section(
        self=current_db_row, current_row_section=None)
    current_db_row.set_city(
        self=current_db_row, current_row_city=None)
    current_db_row.set_state(
        self=current_db_row, current_row_state=None)
    current_db_row.set_postcode(
        self=current_db_row, current_row_postcode=None)
    current_db_row.set_search_level_flag(
        self=current_db_row, current_row_search_level_flag=None)
    current_db_row.set_source(
        self=current_db_row, current_row_source=None)
    current_db_row.set_source_id(
        self=current_db_row, current_row_source_id=None)
    current_db_row.set_salesman(
        self=current_db_row, current_row_salesman=None)
    current_db_row.set_notify_email(
        self=current_db_row, current_row_notify_email=None)
    current_db_row.set_notify_mobile(
        self=current_db_row, current_row_notify_mobile=None)
    current_db_row.set_result_type(
        self=current_db_row, current_row_result_type=None)
    current_db_row.set_result_remark(
        self=current_db_row, current_row_result_remark=None)
    current_db_row.set_is_active(
        self=current_db_row, current_row_is_active=None)
    current_db_row.set_created_at(
        self=current_db_row, current_row_created_at=None)
    current_db_row.set_updated_at(
        self=current_db_row, current_row_updated_at=None)
