from selenium.webdriver.common.by import By


def we_are_not_able_to_proceed_error(driver, a):
    # The page with "Sorry, we are unable to proceed at the moment. This error could be due to loss of connection to the server. Please try again later."
    driver.find_element(
        By.XPATH, "(//div[@class='errorDisplay']//div//table//b//text())[1]")
    link_to_click = driver.find_element(
        By.XPATH, "(//div[@class='errorDisplay']//div//table//tr//td//b//a)[1]")
    a.move_to_element(link_to_click).click().perform()
    return (driver, a)
