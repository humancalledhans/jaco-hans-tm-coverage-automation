from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.tm_partners.singleton.current_db_row import CurrentDBRow

def filter_street(driver, a):
    """Attempting to improve the search results by filtering by street name

    Args:
        driver: selenium driver
        a: ActionChains object

    Returns:
        driver, a
    """
    street_filter_tab = driver.find_element(
        By.XPATH, "//input[@id='flt2_resultAddressGrid' and @type='text' and @class='flt']")
    
    street_clean = _preprocess_street()
    
    street_filter_tab.clear()
    # street_filter_tab.send_keys(street_clean)

    number_of_results = len(driver.find_elements(
        By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style='display: none;')]"))

    # by now we should have the accurate number_of_results reading
    # if the filtering hasn't improved the search
    if number_of_results == 0:
        street_filter_tab.clear()
        street_filter_tab.send_keys(Keys.BACKSPACE)

    return (driver, a)

def _preprocess_street():
    current_db_row = CurrentDBRow.get_instance()
    street = current_db_row.get_street(
        self=current_db_row)    
    street_types = current_db_row.get_accepted_street_types_list(
        self=current_db_row)
    
    # removing street type from street name
    for type in street_types:
        if type in street:
            street = street.replace(type, '')
            break
    street = street.strip()
    
    return street
