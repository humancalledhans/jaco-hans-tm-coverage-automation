from tm_global.singleton.retry_at_end import RetryAtEndCache
from src.tm_global.singleton.current_db_row import CurrentDBRow
from tm_global import tm_global
from src.tm_global.singleton.data_id_range import DataIdRange


def retry_for_current_db_row_at_end():
    current_db_row = CurrentDBRow.get_instance()
    current_row_id = current_db_row.get_id(
        self=current_db_row)
    data_id_range_singleton = DataIdRange.get_instance()
    data_id_range_singleton.set_start_id(
        self=data_id_range_singleton, start_id=current_row_id)
    data_id_range_singleton.set_end_id(
        self=data_id_range_singleton, end_id=current_row_id)
    tm_global()
