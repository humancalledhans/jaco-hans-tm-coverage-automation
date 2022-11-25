from src.tm_global.operations.pause_until_loaded import pause_until_loaded
from src.tm_global.operations.select_state import select_state


def reset_for_next_search(driver, a):
    if (
        driver.current_url
        == "https://wholesalepremium.tm.com.my/coverage-search/result"
    ):
        driver.get("https://wholesalepremium.tm.com.my/coverage-search/address")
        (driver, a) = pause_until_loaded(driver, a)
        try:
            (driver, a) = select_state(driver, a)
            return (driver, a)
        except Exception as e:
            print(e)
    elif (
        driver.current_url == "https://wholesalepremium.tm.com.my/install/search/result"
    ):
        driver.get("https://wholesalepremium.tm.com.my/install/search/address")
        (driver, a) = pause_until_loaded(driver, a)
        try:
            (driver, a) = select_state(driver, a)
            return (driver, a)
        except Exception as e:
            print(e)
    else:
        return (driver, a)
