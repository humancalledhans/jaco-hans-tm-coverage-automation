from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.operations.enter_into_building_name_filter import enter_into_building_name_filter


def filter_by_building_name(driver, a):
    # filter by building name
    current_db_row = CurrentDBRow.get_instance()
    building_name = current_db_row.get_building(self=current_db_row)
    if building_name != '' and len(building_name) > 3 and building_name is not None:
        try:
            (driver, a) = enter_into_building_name_filter(driver, a)
            (driver, a) = pause_until_loaded(driver, a)
        except Exception('Building name filter field did not pop up.'):
            raise Exception('Building name filter field did not pop up.')

    return (driver, a)
