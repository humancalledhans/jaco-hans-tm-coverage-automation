from abc import ABCMeta, abstractstaticmethod
from src.tm_global.db_read_write.db_get_largest_id import get_max_id_from_db
from src.tm_global.db_read_write.db_get_smallest_id import get_min_id_from_db
import threading


class IDataIdRange(metaclass=ABCMeta):
    @abstractstaticmethod
    def set_start_id():
        """to implement in child class"""

    @abstractstaticmethod
    def set_start_id():
        """to implement in child class"""

    @abstractstaticmethod
    def get_start_id():
        """to implement in child class"""

    @abstractstaticmethod
    def get_end_id():
        """to implement in child class"""


class DataIdRange(IDataIdRange):
    @staticmethod
    def get_instance():
        local = threading.current_thread().__dict__
        try:
            instance = local["data_id_range_instance"]
        except KeyError:
            local["data_id_range_instance"] = DataIdRange()
            instance = local["data_id_range_instance"]
        if instance is None:
            instance = DataIdRange()
        return instance

    def __init__(self, start_id=get_min_id_from_db(), end_id=get_max_id_from_db()):
        self.start_id = start_id
        self.end_id = end_id

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
