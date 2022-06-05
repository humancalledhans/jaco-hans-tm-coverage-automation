import os
from PIL import Image
from anticaptchaofficial.imagecaptcha import *


def captcha_decoder(image):

    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key("7b5edfaf9c96fcb48fcc9fd55cee4f41")

    # captcha_text = solver.solve_and_return_solution("captcha.jpeg")
    captcha_text = solver.solve_and_return_solution(image)
    if captcha_text != 0:
        return captcha_text
    else:
        return solver.error_code


def solve_captcha(captcha_elem_to_solve, driver):
    location = captcha_elem_to_solve.location
    size = captcha_elem_to_solve.size

    whole_page_image = driver.save_screenshot('wholePage.png')
    im = Image.open('wholePage.png')

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))
    im.save('captcha.png')

    captcha_code = captcha_decoder("captcha.png")

    os.remove('wholePage.png')
    os.remove('captcha.png')

    return captcha_code
