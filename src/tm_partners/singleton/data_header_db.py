from abc import ABCMeta, abstractstaticmethod
import threading


class IDBDataHeader(metaclass=ABCMeta):
    @abstractstaticmethod
    def set_headers():
        """to implement in child class"""

    @abstractstaticmethod
    def get_headers():
        """to implement in child class"""


class DBDataHeader(IDBDataHeader):
    @staticmethod
    def get_instance():
        local = threading.current_thread().__dict__
        try:
            instance = local["db_data_header_instance"]
        except KeyError:
            local["db_data_header_instance"] = DBDataHeader()
            instance = local["db_data_header_instance"]
        if instance is None:
            instance = DBDataHeader()
        return instance

    def __init__(self):
        self.headers = None

    @staticmethod
    def set_headers(self, headers):
        self.headers = headers

    @staticmethod
    def get_headers(self):
        return self.headers
