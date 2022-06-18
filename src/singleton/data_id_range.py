from abc import ABCMeta, abstractstaticmethod


class IDataIdRange(metaclass=ABCMeta):

    @abstractstaticmethod
    def set_start_id():
        """ to implement in child class """

    @abstractstaticmethod
    def set_start_id():
        """ to implement in child class """

    @abstractstaticmethod
    def get_start_id():
        """ to implement in child class """

    @abstractstaticmethod
    def get_end_id():
        """ to implement in child class """


class DataIdRange(IDataIdRange):

    __instance = None

    @staticmethod
    def get_instance():
        if DataIdRange.__instance == None:
            DataIdRange()
        return DataIdRange.__instance

    def __init__(self, start_id=None, end_id=None):
        if DataIdRange.__instance != None:
            raise Exception(
                "DataIdRange instance cannot be instantiated more than once!")
        else:
            self.start_id = start_id
            self.end_id = end_id
            DataIdRange.__instance = self

    @staticmethod
    def set_start_id(self, start_id):
        self.start_id = start_id

    @staticmethod
    def set_end_id(self, end_id):
        self.end_id = end_id

    @staticmethod
    def get_start_id(self):
        return self.start_id

    @staticmethod
    def get_end_id(self):
        return self.end_id
