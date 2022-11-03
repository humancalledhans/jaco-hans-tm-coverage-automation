from abc import ABCMeta, abstractstaticmethod

from src.tm_partners.db_read_write.db_write_to_cvg_task import write_to_cvg_task


class ICVGTask(metaclass=ABCMeta):

    @abstractstaticmethod
    def set_failed_id():
        """ to implement in child class """

    @abstractstaticmethod
    def set_total_number_of_addresses_to_check():
        """ to implement in child class """

    @abstractstaticmethod
    def increment_total_number_of_addresses_checked():
        """ to implement in child class """

    @abstractstaticmethod
    def write_to_db():
        """ to implement in child class """


class CVGTask(ICVGTask):

    __instance = None

    @staticmethod
    def get_instance():
        if CVGTask.__instance is None:
            CVGTask()
        return CVGTask.__instance

    def __init__(self):
        if CVGTask.__instance is not None:
            raise Exception(
                "CVGTask instance cannot be instantiated more than once!")
        else:
            self.failed_id = None
            self.total_number_of_addresses_to_check = 0
            self.total_number_of_addresses_checked = 0
            CVGTask.__instance = self

    def set_failed_id(self, current_id):
        self.failed_id = current_id

    def set_total_number_of_addresses_to_check(self, total_number_of_addresses_to_check):
        self.total_number_of_addresses_to_check = total_number_of_addresses_to_check

    def increment_total_number_of_addresses_checked(self):
        self.total_number_of_addresses_checked += 1

    def write_to_db(self):
        if self.failed_id is not None:
            write_to_cvg_task(remark=f"Failed at {self.failed_id}",
                              total=self.total_number_of_addresses_to_check, complete=self.total_number_of_addresses_checked)
        else:
            write_to_cvg_task(
                remark='SUCCESS!!', total=self.total_number_of_addresses_to_check, complete=self.total_number_of_addresses_checked)
