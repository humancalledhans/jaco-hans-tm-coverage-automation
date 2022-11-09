def duplicate_in_new_tab(driver, a, root_tab_url):
    driver.execute_script("window.open('');")
    # Switch to the new window and open new URL
    driver.switch_to.window(driver.window_handles[1])
    driver.get(root_tab_url)
    return (driver, a)
