from abc import ABCMeta, abstractstaticmethod


class IAllTheData(metaclass=ABCMeta):

    @abstractstaticmethod
    def add_into_data_list():
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

    def add_into_data_list(self, data):
        """
        Remember that data should be a DataObject object.
        """
        self.all_the_data_list.append(data)

    def get_all_the_data_list(self):
        return self.all_the_data_list
