from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.tm_partners.singleton.current_db_row import CurrentDBRow

def filter_section(driver, a):
    """Attempting to improve the search results by filtering by section

    Args:
        driver: selenium driver
        a: ActionChains object

    Returns:
        driver, a
    """
    section_filter_tab = driver.find_element(
        By.XPATH, "//input[@id='flt3_resultAddressGrid' and @type='text' and @class='flt']")
    
    section_clean = _preprocess_section()
    
    section_filter_tab.clear()
    section_filter_tab.send_keys(section_clean)

    number_of_results = len(driver.find_elements(
        By.XPATH, "//table[@id='resultAddressGrid']//tr[@class='odd' or @class='even'][not(@style='display: none;')]"))

    # by now we should have the accurate number_of_results reading
    # if the filtering hasn't improved the search
    if number_of_results == 0:
        section_filter_tab.clear()
        section_filter_tab.send_keys(Keys.BACKSPACE)

    return (driver, a)

def _preprocess_section():
    current_db_row = CurrentDBRow.get_instance()
    section = current_db_row.get_section(
        self=current_db_row)
    
    return section
