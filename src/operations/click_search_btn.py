from selenium.webdriver.common.by import By

def click_search_btn(driver, a):
    search_btn_third_col = driver.find_element(
        By.XPATH, "//form[@name='Netui_Form_3']//img[contains(@src, 'btnSearchBlue') and @alt='Search']")
    a.move_to_element(search_btn_third_col).click().perform()
    return (driver, a)
