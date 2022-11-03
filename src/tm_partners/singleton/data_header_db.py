from abc import ABCMeta, abstractstaticmethod


class IDBDataHeader(metaclass=ABCMeta):

    @abstractstaticmethod
    def set_headers():
        """ to implement in child class """

    @abstractstaticmethod
    def get_headers():
        """ to implement in child class """


class DBDataHeader(IDBDataHeader):

    __instance = None

    @staticmethod
    def get_instance():
        if DBDataHeader.__instance == None:
            DBDataHeader()
        return DBDataHeader.__instance

    def __init__(self):
        if DBDataHeader.__instance != None:
            raise Exception(
                "DBDataHeader instance cannot be instantiated more than once!")
        else:
            DBDataHeader.__instance = self

    @staticmethod
    def set_headers(self, headers):
        self.headers = headers

    @staticmethod
    def get_headers(self):
        return self.headers
