from abc import ABCMeta, abstractstaticmethod


class IAllTheData(metaclass=ABCMeta):

    @abstractstaticmethod
    def add_into_data_list():
        """ to implement in child class """

    @abstractstaticmethod
    def set_data_list():
        """ to implement in child class """

    @abstractstaticmethod
    def get_all_the_data_list():
        """ to implement in child class """

    @staticmethod
    def reset_all_data():
        """ to implement in child class """


class AllTheData(IAllTheData):

    __instance = None

    @staticmethod
    def get_instance():
        if AllTheData.__instance is None:
            AllTheData()
        return AllTheData.__instance

    def __init__(self):
        if AllTheData.__instance is not None:
            raise Exception(
                "AllTheData instance cannot be instantiated more than once!")
        else:
            self.all_the_data_list = []
            AllTheData.__instance = self

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
