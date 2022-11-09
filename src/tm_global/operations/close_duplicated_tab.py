def close_duplicated_tab(driver, a):
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return (driver, a)
