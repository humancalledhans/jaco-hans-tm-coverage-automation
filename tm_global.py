import threading
import time
import sys
from src.tm_global.singleton.num_of_iterations import NumOfIterations
from src.tm_global.singleton.data_id_range import DataIdRange

# from src.tm_global.operations.thread_asgn import ThreadAsgn
from src.tm_global.operations.driver_setup import tm_global_driver_setup
from src.tm_global.operations.tm_global_login import TMGlobalLogin
from src.tm_global.operations.retry_problematic_addresses import (
    retry_problematic_address,
)

from selenium.webdriver import ActionChains

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotInteractableException

from src.tm_global.operations.go_to_coverage_search_page import to_coverage_search_page
from src.tm_global.db_read_write.db_read_address import read_from_db
from src.tm_global.coverage_check.coverage_check import finding_coverage
from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.db_read_write.db_get_largest_id import get_max_id_from_db
from src.tm_global.db_read_write.db_get_smallest_id import get_min_id_from_db


class TMGlobalThreadAsgn:
    # def __init__(self, ids_to_start_from=1373, ids_to_end_at=1373):
    def __init__(
        self, ids_to_start_from=get_min_id_from_db(), ids_to_end_at=get_max_id_from_db()
    ):
        self.ids_to_start_from = ids_to_start_from
        self.ids_to_end_at = ids_to_end_at
        read_from_db()

    def main_thread(
        self,
        thread_ids_to_start_from=get_min_id_from_db(),
        thread_ids_to_end_at=get_max_id_from_db(),
    ):
        tm_global(thread_ids_to_start_from, thread_ids_to_end_at)

    def start_threads(self, number_of_threads=1):
        # threading.Thread(target=self.main_thread).start()
        number_of_ids_to_check = self.ids_to_end_at - self.ids_to_start_from

        print("NUM OF INSTANCES", number_of_threads)

        print("num of ids to check", number_of_ids_to_check)

        # split the ids to check into equal parts for each thread.
        # add remainder to the last thread.
        ids_to_check_per_thread = number_of_ids_to_check // number_of_threads
        remainder = number_of_ids_to_check % number_of_threads

        for i in range(number_of_threads):
            thread_ids_to_start_from = self.ids_to_start_from + (
                ids_to_check_per_thread * i
            )
            thread_ids_to_end_at = thread_ids_to_start_from + ids_to_check_per_thread

            if i == number_of_threads - 1:
                thread_ids_to_end_at += remainder

            print(
                "thread_ids_to_start_from",
                thread_ids_to_start_from,
                "thread_ids_to_end_at",
                thread_ids_to_end_at,
            )

            threading.Thread(
                target=self.main_thread,
                args=(thread_ids_to_start_from, thread_ids_to_end_at),
            ).start()


def tm_global(thread_ids_to_start_from, thread_ids_to_end_at):

    # data_id_range_instance = DataIdRange.get_instance()
    # data_id_range_instance.set_start_id(
    #     self=data_id_range_instance, start_id=int(thread_ids_to_start_from))
    # data_id_range_instance.set_end_id(self=data_id_range_instance,
    #                                   end_id=int(thread_ids_to_end_at))

    # def tm_global():

    local = threading.current_thread().__dict__

    local["data_id_range_instance"] = data_id_range_instance

    # Step 1: read from database.

    # Step 2: set up Chrome browser instance for Selenium.
    driver = tm_global_driver_setup()

    website_loaded = False
    while not website_loaded:
        try:
            driver.get("https://wholesalepremium.tm.com.my/")
            a = ActionChains(driver)
            (driver, a) = pause_until_loaded(driver, a)
            website_loaded = True

        except WebDriverException:
            print("failed. try again-")
            time.sleep(100)

    login = TMGlobalLogin("avenda1", "123")
    (driver, a) = login.login(driver, a)

    (driver, a) = to_coverage_search_page(driver, a)

    try:
        # Step 3: coverage check.
        finding_coverage(driver, a)
    except ElementNotInteractableException:
        print("element not interactable exception")
        time.sleep(5000)

    # retrying problematic id-s.
    retry_problematic_address()

    # Step 4: write to database.
    # write_results_to_db()

    # we are at the coverage search page now.
    # finding_coverage = FindingCoverage()
    # set_accepted_params()
    # # read_from_db()
    # finding_coverage.finding_coverage(
    #     driver=driver, a=a)


# importable lock variable (can be used in other files)
tm_global_lock = threading.Lock()

if __name__ == "__main__":

    # if an item in argument is --count, get the next item in the list.
    num_of_threads = None
    if "--count" in sys.argv:
        num_of_threads = int(sys.argv[sys.argv.index("--count") + 1])

    if num_of_threads is None:
        num_of_threads = 2

    num_of_iterations = 1  # jaco, change this line.
    num_of_iterations_instance = NumOfIterations.get_instance()
    num_of_iterations_instance.set_num_of_iterations(int(num_of_iterations))
    tm_global()
    # thread_asgn = TMGlobalThreadAsgn()
    # thread_asgn.start_threads()

    # x = threading.Thread(target=func)
    # x.start()
    # print(threading.active_count())
