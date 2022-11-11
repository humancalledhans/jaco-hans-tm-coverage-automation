from abc import ABCMeta, abstractstaticmethod


class IRetryAtEndCache(metaclass=ABCMeta):
    @abstractstaticmethod
    def add_data_id_to_retry():
        """ to implement in child class """

    @abstractstaticmethod
    def get_data_id_list_to_retry():
        """ to implement in child class """


class RetryAtEndCache(IRetryAtEndCache):

    __instance = None

    @staticmethod
    def get_instance():
        if RetryAtEndCache.__instance is None:
            RetryAtEndCache()
        return RetryAtEndCache.__instance

    def __init__(self):
        if RetryAtEndCache.__instance is not None:
            raise Exception(
                "RetryAtEndCache instance cannot be instantiated more than once!")
        else:
            RetryAtEndCache.__instance = self
            self.data_ids_to_retry = []

    @staticmethod
    def add_data_id_to_retry(self, data_id):
        self.data_ids_to_retry.append(data_id)

    @staticmethod
    def get_data_id_list_to_retry(self):
        return self.data_ids_to_retry
