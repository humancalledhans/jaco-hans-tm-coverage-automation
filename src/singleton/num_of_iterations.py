from abc import ABCMeta, abstractstaticmethod


class INumOfIterations(metaclass=ABCMeta):

    @abstractstaticmethod
    def set_num_of_iterations():
        """ to implement in child class """


class NumOfIterations(INumOfIterations):

    __instance = None

    @staticmethod
    def get_instance():
        if NumOfIterations.__instance is None:
            NumOfIterations()
        return NumOfIterations.__instance

    def __init__(self):
        if NumOfIterations.__instance is not None:
            raise Exception(
                "NumOfIterations instance cannot be instantiated more than once!")
        else:
            self.num_of_iterations = 0
            NumOfIterations.__instance = self

    def set_num_of_iterations(self, data):
        self.num_of_iterations = data

    def get_num_of_iterations(self):
        return self.num_of_iterations
