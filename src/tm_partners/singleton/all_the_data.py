from abc import ABCMeta, abstractstaticmethod
import threading


class IAllTheData(metaclass=ABCMeta):
    @abstractstaticmethod
    def add_into_data_list():
        """to implement in child class"""

    @abstractstaticmethod
    def set_data_list():
        """to implement in child class"""

    @abstractstaticmethod
    def get_all_the_data_list():
        """to implement in child class"""

    @staticmethod
    def reset_all_data():
        """to implement in child class"""


class AllTheData(IAllTheData):
    @staticmethod
    def get_instance():
        local = threading.current_thread().__dict__
        try:
            instance = local["all_the_data_instance"]
        except KeyError:
            local["all_the_data_instance"] = AllTheData()
            instance = local["all_the_data_instance"]
        if instance is None:
            instance = AllTheData()
        return instance

    def __init__(self):
        self.all_the_data_list = []

    @staticmethod
    def add_into_data_list(self, data):
        """
        Remember that data should be a DataObject object.
        """
        self.all_the_data_list.append(data)

    @staticmethod
    def set_data_list(self, data_list):
        self.all_the_data_list = data_list

    @staticmethod
    def get_all_the_data_list(self):
        return self.all_the_data_list

    @staticmethod
    def reset_all_data(self):
        self.all_the_data_list = []
