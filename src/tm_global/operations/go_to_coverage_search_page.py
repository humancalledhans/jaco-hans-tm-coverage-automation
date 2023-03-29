from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def to_coverage_search_page(driver, a):
    driver.get("https://wholesalepremium.tm.com.my/install/search/address")
    (driver1, a1) = pause_until_loaded(driver, a)
    return (driver1, a1)
