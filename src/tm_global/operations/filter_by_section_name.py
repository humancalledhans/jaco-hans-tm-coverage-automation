from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.operations.enter_into_section_name_filter import enter_into_section_name_filter


def filter_by_section_name(driver, a):
    # filter by street name
    current_db_row = CurrentDBRow.get_instance()
    section_name = current_db_row.get_section(self=current_db_row)
    if section_name != '' and len(section_name) > 3 and section_name is not None:
        try:
            (driver, a) = enter_into_section_name_filter(driver, a)
            (driver, a) = pause_until_loaded(driver, a)
        except Exception('Section name filter field did not pop up.'):
            raise Exception('Section name filter field did not pop up.')

    return (driver, a)
