from src.tm_global.singleton.current_input_row import CurrentInputRow
from src.tm_global.operations.enter_into_lot_no_filter import enter_into_lot_number_filter
from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def filter_by_lot_number(driver, a):
    # filter by lot number.
    current_input_row = CurrentInputRow.get_instance()
    lot_number = current_input_row.get_house_unit_lotno(self=current_input_row)
    if lot_number != '' and lot_number is not None:
        (driver, a) = enter_into_lot_number_filter(driver, a)
        (driver, a) = pause_until_loaded(driver, a)

    return (driver, a)
