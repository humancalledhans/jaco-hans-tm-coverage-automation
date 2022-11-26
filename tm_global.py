import threading
import time
from src.tm_global.singleton.num_of_iterations import NumOfIterations
from src.tm_global.singleton.data_id_range import DataIdRange
# from src.tm_global.operations.thread_asgn import ThreadAsgn
from src.tm_global.operations.driver_setup import tm_global_driver_setup
from src.tm_global.operations.tm_global_login import TMGlobalLogin
from src.tm_global.operations.retry_problematic_addresses import retry_problematic_address

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
    def __init__(self, ids_to_start_from=get_min_id_from_db(), ids_to_end_at=get_max_id_from_db()):
        self.ids_to_start_from = ids_to_start_from
        self.ids_to_end_at = ids_to_end_at
        read_from_db()
        # data_id_range = DataIdRange.get_instance()
        # data_id_range.set_start_id(
        #     self=data_id_range, start_id=int(ids_to_start_from))
        # data_id_range.set_end_id(self=data_id_range,
        #                          end_id=int(ids_to_end_at))

    def main_thread(self, thread_ids_to_start_from=get_min_id_from_db(), thread_ids_to_end_at=get_max_id_from_db(), thread_name=None):
        tm_global(thread_ids_to_start_from, thread_ids_to_end_at, thread_name)

    def start_threads(self):
        # threading.Thread(target=self.main_thread).start()
        number_of_ids_to_check = self.ids_to_end_at - self.ids_to_start_from

        number_of_threads = 1
        for num in range(30, 0, -1):
            if number_of_ids_to_check % num == 0:
                number_of_threads = num

        print("NUM OF INSTANCES", number_of_threads)

        if number_of_ids_to_check < 4:
            threading.Thread(target=self.main_thread, args=(
                self.ids_to_start_from, self.ids_to_end_at, "thread-1")).start()

        elif number_of_ids_to_check % 13 == 0:
            threading.Thread(target=self.main_thread, args=(
                self.ids_to_start_from, int(self.ids_to_end_at / 13), "thread-1")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at / 13), int(self.ids_to_end_at * 2 / 13), "thread-2")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 2 / 13), int(self.ids_to_end_at * 3 / 13), "thread-3")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 3 / 13), int(self.ids_to_end_at * 4 / 13), "thread-4")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 4 / 13), int(self.ids_to_end_at * 5 / 13), "thread-5")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 5 / 13), int(self.ids_to_end_at * 6 / 13), "thread-6")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 6 / 13), int(self.ids_to_end_at * 7 / 13), "thread-7")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 7 / 13), int(self.ids_to_end_at * 8 / 13), "thread-8")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 8 / 13), int(self.ids_to_end_at * 9 / 13), "thread-9")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 9 / 13), int(self.ids_to_end_at * 10 / 13), "thread-10")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 10 / 13), int(self.ids_to_end_at * 11 / 13), "thread-11")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 11 / 13), int(self.ids_to_end_at * 12 / 13), "thread-12")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 12 / 13), self.ids_to_end_at, "thread-13")).start()

        elif number_of_ids_to_check % 7 == 0:
            threading.Thread(target=self.main_thread, args=(
                self.ids_to_start_from, int(self.ids_to_end_at / 7), "thread-1")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at / 7), int(self.ids_to_end_at * 2 / 7), "thread-2")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 2 / 7), int(self.ids_to_end_at * 3 / 7), "thread-3")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 3 / 7), int(self.ids_to_end_at * 4 / 7), "thread-4")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 4 / 7), int(self.ids_to_end_at * 5 / 7), "thread-5")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 5 / 7), int(self.ids_to_end_at * 6 / 7), "thread-6")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 6 / 7), self.ids_to_end_at, "thread-7")).start()

        elif number_of_ids_to_check % 5 == 0:
            threading.Thread(target=self.main_thread, args=(
                self.ids_to_start_from, int(self.ids_to_end_at / 5), "thread-1")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at / 5), int(self.ids_to_end_at * 2 / 5), "thread-2")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 2 / 5), int(self.ids_to_end_at * 3 / 5), "thread-3")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 3 / 5), int(self.ids_to_end_at * 4 / 5), "thread-4")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 4 / 5), self.ids_to_end_at, "thread-5")).start()

        elif number_of_ids_to_check % 4 == 0:
            threading.Thread(target=self.main_thread, args=(
                self.ids_to_start_from, int(self.ids_to_end_at / 4), "thread-1")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at / 4), int(self.ids_to_end_at / 2), "thread-2")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at / 2), int(self.ids_to_end_at * 3 / 4), "thread-3")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 3 / 4), self.ids_to_end_at, "thread-4")).start()

        elif number_of_ids_to_check % 3 == 0:
            threading.Thread(target=self.main_thread, args=(
                self.ids_to_start_from, int(self.ids_to_end_at / 3), "thread-1")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at / 3), int(self.ids_to_end_at * 2 / 3), "thread-2")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at * 2 / 3), self.ids_to_end_at, "thread-3")).start()

        elif number_of_ids_to_check % 2 == 0:
            threading.Thread(target=self.main_thread, args=(
                self.ids_to_start_from, int(self.ids_to_end_at / 2), "thread-1")).start()
            threading.Thread(target=self.main_thread, args=(
                int(self.ids_to_end_at / 2), self.ids_to_end_at, "thread-2")).start()

        # threading.Thread(target=self.main_thread, args=(
        #     self.ids_to_start_from, self.ids_to_end_at//number_of_threads * 1, "thread-1")).start()

        # for num_of_instance in range(1, number_of_threads+1):
        #     threading.Thread(target=self.main_thread, args=(self.ids_to_end_at//number_of_threads * num_of_instance,
        #                      self.ids_to_end_at//number_of_threads * num_of_instance+1, f"thread-{num_of_instance}")).start()


# def tm_global(thread_ids_to_start_from, thread_ids_to_end_at, thread_name):
def tm_global():

    # data_id_range_instance = DataIdRange.get_instance()
    # data_id_range_instance.set_start_id(
    #     self=data_id_range_instance, start_id=int(thread_ids_to_start_from))
    # data_id_range_instance.set_end_id(self=data_id_range_instance,
    #                                   end_id=int(thread_ids_to_end_at))

    # def tm_global():

    # Step 1: read from database.

    # Step 2: set up Chrome browser instance for Selenium.
    driver = tm_global_driver_setup()

    website_loaded = False
    while not website_loaded:
        try:
            driver.get('https://wholesalepremium.tm.com.my/')
            a = ActionChains(driver)
            (driver, a) = pause_until_loaded(driver, a)
            website_loaded = True

        except WebDriverException:
            print('failed. try again-')
            time.sleep(100)

    login = TMGlobalLogin('avenda1', '123')
    (driver, a) = login.login(driver, a)

    (driver, a) = to_coverage_search_page(driver, a)

    try:
        # Step 3: coverage check.
        finding_coverage(driver, a)
    except ElementNotInteractableException:
        print('element not interactable exception')
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
if __name__ == '__main__':
    num_of_iterations = 1  # jaco, change this line.
    num_of_iterations_instance = NumOfIterations.get_instance()
    num_of_iterations_instance.set_num_of_iterations(int(num_of_iterations))
    tm_global()
    # thread_asgn = TMGlobalThreadAsgn()
    # thread_asgn.start_threads()

    # x = threading.Thread(target=func)
    # x.start()
    # print(threading.activeCount())
