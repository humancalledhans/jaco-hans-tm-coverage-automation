from src.tm_global.operations.pause_until_loaded import pause_until_loaded


def return_to_coverage_search_page(driver, a):
    if (
        driver.current_url
        == "https://wholesalepremium.tm.com.my/coverage-search/result"
    ):
        driver.get("https://wholesalepremium.tm.com.my/coverage-search/address")
    elif (
        driver.current_url == "https://wholesalepremium.tm.com.my/install/search/result"
    ):
        driver.get("https://wholesalepremium.tm.com.my/install/search/address")
    (driver, a) = pause_until_loaded(driver, a)
    return (driver, a)
