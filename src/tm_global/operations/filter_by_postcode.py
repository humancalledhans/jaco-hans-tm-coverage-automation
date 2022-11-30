from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.operations.enter_into_postcode_filter import (
    enter_into_postcode_filter,
)


def filter_by_postcode(driver, a):
    # filter by street name
    current_db_row = CurrentDBRow.get_instance()
    city_name = current_db_row.get_city(self=current_db_row)
    if city_name != "" and len(city_name) > 3 and city_name is not None:
        try:
            (driver, a) = enter_into_postcode_filter(driver, a)
            (driver, a) = pause_until_loaded(driver, a)
        except Exception("Postcode filter field did not pop up."):
            raise Exception("Postcode filter field did not pop up.")

    return (driver, a)
