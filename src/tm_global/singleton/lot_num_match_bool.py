from abc import ABCMeta, abstractstaticmethod


class ILotNumMatchBool(metaclass=ABCMeta):

    @abstractstaticmethod
    def set_lotnummatch():
        """ to implement in child class """

    @abstractstaticmethod
    def get_lotnummatch():
        """ to implement in child class """

    @staticmethod
    def reset_lotnummatch():
        """ to implement in child class """


class LotNumMatchBool(ILotNumMatchBool):

    __instance = None

    @staticmethod
    def get_instance():
        if LotNumMatchBool.__instance is None:
            LotNumMatchBool()
        return LotNumMatchBool.__instance

    def __init__(self):
        if LotNumMatchBool.__instance is not None:
            raise Exception(
                "LotNumMatchBool instance cannot be instantiated more than once!")
        else:
            self.lotnummatch = None
            LotNumMatchBool.__instance = self

    @staticmethod
    def set_lotnummatch(self, lotnummatch):
        self.lotnummatch = lotnummatch

    @staticmethod
    def get_lotnummatch(self):
        return self.lotnummatch

    @staticmethod
    def reset_lotnummatch(self):
        self.lotnummatch = None
