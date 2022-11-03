from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def return_to_coverage_search_page(driver, a):
    driver.get("https://wholesalepremium.tm.com.my/coverage-search/address")
    (driver, a) = pause_until_loaded(driver, a)
    return (driver, a)
