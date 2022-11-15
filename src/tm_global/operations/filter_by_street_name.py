from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.operations.enter_into_street_name_filter import enter_into_street_name_filter


def filter_by_street_name(driver, a):
    # filter by street name
    current_db_row = CurrentDBRow.get_instance()
    street_name = current_db_row.get_street(self=current_db_row)
    if street_name != '' and len(street_name) > 3 and street_name is not None:
        try:
            (driver, a) = enter_into_street_name_filter(driver, a)
            (driver, a) = pause_until_loaded(driver, a)
        except Exception('Street name filter field did not pop up.'):
            raise Exception('Street name filter field did not pop up.')

    return (driver, a)
