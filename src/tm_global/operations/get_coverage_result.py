import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def get_coverage_result(driver, a):
    result_remark = driver.find_element(
        By.XPATH, "(//div[@class='col-lg-6 offset-lg-1 text-center']//p)[1]").text
    try:
        result_description = driver.find_element(
            By.XPATH, "//p[@class='mb-0']").text
        if result_description == 'Sorry, the address in our database is incomplete based on your inputs. Please try searching again.':
            result_remark = result_description
    except NoSuchElementException:
        pass
    result_type = 0

    time.sleep(3)
    print('result remark', result_remark)
    return (result_type, result_remark)
