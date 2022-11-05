from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.enter_into_lot_no_filter import enter_into_lot_number_filter
from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def filter_by_lot_number(driver, a):
    # filter by lot number.
    current_db_row = CurrentDBRow.get_instance()
    lot_number = current_db_row.get_house_unit_lotno(self=current_db_row)
    if lot_number != '' and lot_number is not None:
        (driver, a) = enter_into_lot_number_filter(driver, a)
        (driver, a) = pause_until_loaded(driver, a)

    return (driver, a)
