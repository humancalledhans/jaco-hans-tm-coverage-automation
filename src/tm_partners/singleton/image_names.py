from abc import ABCMeta, abstractstaticmethod
import threading


class IImageName(metaclass=ABCMeta):
    @abstractstaticmethod
    def set_full_page_image_name():
        """to implement in child class"""

    @abstractstaticmethod
    def set_captcha_image_name():
        """to implement in child class"""

    @abstractstaticmethod
    def get_full_page_image_name():
        """to implement in child class"""

    @abstractstaticmethod
    def get_captcha_image_name():
        """to implement in child class"""


class ImageName(IImageName):

    __instance = None

    @staticmethod
    def get_instance():
        local = threading.current_thread().__dict__
        try:
            instance = local["image_name_instance"]
        except KeyError:
            local["image_name_instance"] = ImageName()
            instance = local["image_name_instance"]
        if instance is None:
            instance = ImageName()
        return instance

    def __init__(self):
        self.full_page_image_name = None
        self.captcha_image_name = None

    @staticmethod
    def set_full_page_image_name(self, full_page_image_name):
        self.full_page_image_name = full_page_image_name

    @staticmethod
    def set_captcha_image_name(self, captcha_image_name):
        self.captcha_image_name = captcha_image_name

    @staticmethod
    def get_full_page_image_name(self):
        return self.full_page_image_name

    @staticmethod
    def get_captcha_image_name(self):
        return self.captcha_image_name
