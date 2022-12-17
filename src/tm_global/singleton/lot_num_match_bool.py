from abc import ABCMeta, abstractstaticmethod
import threading


class ILotNumMatchBool(metaclass=ABCMeta):
    @abstractstaticmethod
    def set_lotnummatch():
        """to implement in child class"""

    @abstractstaticmethod
    def get_lotnummatch():
        """to implement in child class"""

    @staticmethod
    def reset_lotnummatch():
        """to implement in child class"""


class LotNumMatchBool(ILotNumMatchBool):
    @staticmethod
    def get_instance():
        local = threading.current_thread().__dict__
        try:
            instance = local["lot_num_match_bool_instance"]
        except KeyError:
            local["lot_num_match_bool_instance"] = LotNumMatchBool()
            instance = local["lot_num_match_bool_instance"]
        if instance is None:
            instance = LotNumMatchBool()
        return instance

    def __init__(self):
        self.lotnummatch = None

    @staticmethod
    def set_lotnummatch(self, lotnummatch):
        self.lotnummatch = lotnummatch

    @staticmethod
    def get_lotnummatch(self):
        return self.lotnummatch

    @staticmethod
    def reset_lotnummatch(self):
        self.lotnummatch = None
