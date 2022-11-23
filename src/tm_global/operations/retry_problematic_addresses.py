# from src.tm_global.operations.thread_asgn import ThreadAsgn
from src.tm_global.operations.driver_setup import tm_global_driver_setup
from src.tm_global.operations.tm_global_login import TMGlobalLogin

from selenium.webdriver import ActionChains

from src.tm_global.operations.go_to_coverage_search_page import to_coverage_search_page
from src.tm_global.coverage_check.coverage_check import finding_coverage
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.singleton.retry_at_end import RetryAtEndCache
from src.tm_global.singleton.data_id_range import DataIdRange


# as of 9th November, not fully tested.
def retry_problematic_address():
    retry_at_end_cache_singleton = RetryAtEndCache.get_instance()
    id_list_to_retry = retry_at_end_cache_singleton.get_data_id_list_to_retry(
        self=retry_at_end_cache_singleton)
    if len(id_list_to_retry) > 0:
        driver = tm_global_driver_setup()
        driver.get('https://wholesalepremium.tm.com.my/')
        a = ActionChains(driver)
        (driver, a) = pause_until_loaded(driver, a)
        login = TMGlobalLogin('avenda1', '123')
        (driver, a) = login.login(driver, a)

        for id in id_list_to_retry:
            data_id_range_singleton = DataIdRange.get_instance()
            data_id_range_singleton.set_start_id(
                self=data_id_range_singleton, start_id=int(id))
            data_id_range_singleton.set_end_id(
                self=data_id_range_singleton, end_id=int(id))

            (driver, a) = to_coverage_search_page(driver, a)

            # Step 3: coverage check.
            finding_coverage(driver, a)
