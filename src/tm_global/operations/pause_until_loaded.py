import time

def pause_until_loaded(driver, a):
    while driver.execute_script("return document.readyState;") != "complete":
        time.sleep(0.5)

    return (driver, a)
