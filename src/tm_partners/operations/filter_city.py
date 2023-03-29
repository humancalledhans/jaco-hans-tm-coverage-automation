from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.tm_partners.singleton.current_db_row import CurrentDBRow

def filter_city(driver, a):
    """Attempting to improve the search results by filtering by city

    Args:
        driver: selenium driver
        a: ActionChains object

    Returns:
        driver, a
    """
    city_filter_tab = driver.find_element(
        By.XPATH, "//input[@id='flt6_resultAddressGrid' and @type='text' and @class='flt']")
    
    city_clean = _preprocess_city()
    
    city_filter_tab.clear()
    city_filter_tab.send_keys(city_clean)

    number_of_results = len(driver.find_elements(
        By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style='display: none;')]"))

    # by now we should have the accurate number_of_results reading
    # if the filtering hasn't improved the search
    if number_of_results == 0:
        city_filter_tab.clear()
        city_filter_tab.send_keys(Keys.BACKSPACE)

    return (driver, a)

def _preprocess_city():
    current_db_row = CurrentDBRow.get_instance()
    city = current_db_row.get_city(
        self=current_db_row)
    
    return city
