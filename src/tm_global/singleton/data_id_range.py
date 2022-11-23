from abc import ABCMeta, abstractstaticmethod
from src.tm_global.db_read_write.db_get_largest_id import get_max_id_from_db
from src.tm_global.db_read_write.db_get_smallest_id import get_min_id_from_db


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

    def __init__(self, start_id=get_min_id_from_db(), end_id=get_max_id_from_db()):
    # def __init__(self, start_id=get_max_id_from_db()//8 *7 , end_id=get_max_id_from_db() // 8 * 8):
    # def __init__(self, start_id=31, end_id=31):
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
