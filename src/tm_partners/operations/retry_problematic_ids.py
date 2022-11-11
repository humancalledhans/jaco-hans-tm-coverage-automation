from src.main import Main
from src.tm_partners.singleton.data_id_range import DataIdRange
from src.tm_partners.singleton.retry_at_end import RetryAtEndCache


def retry_problematic_ids(thread_name):
    retry_at_end_singleton = RetryAtEndCache.get_instance()
    problematic_id_list = retry_at_end_singleton.get_data_id_list_to_retry(
        self=retry_at_end_singleton)

    for problematic_id in problematic_id_list:
        data_id_range = DataIdRange.get_instance()
        data_id_range.set_start_id(
            self=data_id_range, start_id=int(problematic_id))
        data_id_range.set_end_id(
            self=data_id_range, end_id=int(problematic_id))
        Main(thread_name)
