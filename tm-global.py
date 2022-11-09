import time
from src.tm_global.singleton.num_of_iterations import NumOfIterations

# from src.tm_global.operations.thread_asgn import ThreadAsgn
from src.tm_global.operations.tm_global_driver_setup import tm_global_driver_setup
from src.tm_global.operations.tm_global_login import TMGlobalLogin

from selenium.webdriver import ActionChains

from src.tm_partners.operations.go_to_coverage_search_page import to_coverage_search_page
from src.tm_global.operations.set_accepted_params import set_accepted_params
from src.tm_global.db_read_write.db_read_address import read_from_db
from src.tm_global.coverage_check.coverage_check import finding_coverage
from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def tm_global():

    # Step 1: read from database.
    read_from_db()
    set_accepted_params()

    # Step 2: set up Chrome browser instance for Selenium.
    driver = tm_global_driver_setup()
    driver.get('https://wholesalepremium.tm.com.my/')
    a = ActionChains(driver)
    (driver, a) = pause_until_loaded(driver, a)
    login = TMGlobalLogin('avenda1', '123')
    (driver, a) = login.login(driver, a)

    (driver, a) = to_coverage_search_page(driver, a)

    # Step 3: coverage check.
    (driver, a) = finding_coverage(driver, a)

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

    # x = threading.Thread(target=func)
    # x.start()
    # print(threading.activeCount())
