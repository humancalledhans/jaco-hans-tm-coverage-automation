from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def driver_setup():
    s = Service(ChromeDriverManager().install())
    options = Options()
    options.headless = False
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--force-device-scale-factor=1')
    options.add_argument("--no-sandbox")
    options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=s, options=options)
    
    return driver
