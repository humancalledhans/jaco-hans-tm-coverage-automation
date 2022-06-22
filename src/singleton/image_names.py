from abc import ABCMeta, abstractstaticmethod


class IImageName(metaclass=ABCMeta):

    @abstractstaticmethod
    def set_full_page_image_name():
        """ to implement in child class """

    @abstractstaticmethod
    def set_captcha_image_name():
        """ to implement in child class """

    @abstractstaticmethod
    def get_full_page_image_name():
        """ to implement in child class """

    @abstractstaticmethod
    def get_captcha_image_name():
        """ to implement in child class """


class ImageName(IImageName):

    __instance = None

    @staticmethod
    def get_instance():
        if ImageName.__instance == None:
            ImageName()
        return ImageName.__instance

    def __init__(self):
        if ImageName.__instance != None:
            raise Exception(
                "ImageName instance cannot be instantiated more than once!")
        else:
            ImageName.__instance = self

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
