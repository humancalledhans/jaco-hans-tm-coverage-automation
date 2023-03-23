import os
from PIL import Image
from anticaptchaofficial.imagecaptcha import *
from src.tm_partners.operations.pause_until_loaded import pause_until_loaded
from src.tm_partners.singleton.image_names import ImageName

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


def captcha_decoder(image):

    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key("f2b4bd71647468041dfc88de2dbef10b")

    # captcha_text = solver.solve_and_return_solution("captcha.jpeg")
    captcha_text = solver.solve_and_return_solution(image)
    if captcha_text != 0:
        return captcha_text
    else:
        return solver.error_code


def solve_captcha(captcha_elem_to_solve, driver):
    location = captcha_elem_to_solve.location
    size = captcha_elem_to_solve.size

    image_name = ImageName.get_instance()

    # hopefully this would prevent the captchas screenshots from being only HALF opaque.
    time.sleep(0.5)
    whole_page_image = driver.save_screenshot(
        image_name.get_full_page_image_name(self=image_name))
    im = Image.open(image_name.get_full_page_image_name(self=image_name))

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))
    im.save(image_name.get_captcha_image_name(self=image_name))

    captcha_code = captcha_decoder(
        image_name.get_captcha_image_name(self=image_name))

    os.remove(image_name.get_full_page_image_name(self=image_name))
    os.remove(image_name.get_captcha_image_name(self=image_name))

    return captcha_code


def detecting_captcha_and_solve(driver, a, error_message):
    to_proceed = False
    retry_times = 0
    while to_proceed == False:
        try:
            (driver, a) = pause_until_loaded(driver, a)
            captcha_to_solve = WebDriverWait(driver, 0.3).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='blockUI blockMsg blockPage']//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[@src='jcaptchaCustom.jpg' and @border='1']")))
            captcha_code = solve_captcha(
                captcha_elem_to_solve=captcha_to_solve, driver=driver)
            # print("HERE8")
            captcha_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//input[@type='text']")))
            captcha_field.clear()
            captcha_field.send_keys(captcha_code)
            submit_captcha_button = driver.find_element(
                By.XPATH, "//div[@id='layover' and @align='center']//form[@name='Netui_Form_4' and @id='Netui_Form_4']//img[contains(@src, 'btnGo')]")
            a.move_to_element(submit_captcha_button).click().perform()

            try:
                (driver, a) = pause_until_loaded(driver, a)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                    (By.XPATH, "//font[@color='red' and contains(text(), 'The code you entered previously is incorrect. Please try again.')]")))
                retry_times += 1
                if retry_times == 5:
                    print("RETRY_TIMES > 5. WEBSITE IS REFRESHING")
                    # raise Exception("Unable to solve captcha after 5 attempts. Refreshing page...")
                    driver.refresh()
                    (driver, a) = pause_until_loaded(driver, a)
                    retry_times = 0
            except TimeoutException:
                to_proceed = True
                # break

        except TimeoutException:
            retry_times = retry_times + 1
            if retry_times > 5:
                raise Exception(
                    error_message
                )

    return (driver, a)
