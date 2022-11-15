import time
from selenium.webdriver.common.by import By


def get_coverage_result(driver, a):
    result_remark = driver.find_element(
        By.XPATH, "(//div[@class='col-lg-6 offset-lg-1 text-center']//p)[1]").text
    result_type = 0

    print('result remark', result_remark)
    return (result_type, result_remark)
