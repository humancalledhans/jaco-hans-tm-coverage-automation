from abc import ABCMeta, abstractstaticmethod

from src.db_read_write.db_write_to_cvg_task import write_to_cvg_task


class ICVGTask(metaclass=ABCMeta):

    @abstractstaticmethod
    def set_current_id_address_being_checked():
        """ to implement in child class """

    @abstractstaticmethod
    def increment_current_number_of_addresses_checked():
        """ to implement in child class """

    @abstractstaticmethod
    def increment_completed_addresses():
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
            self.current_id_address_being_checked = None
            self.total_number_of_addresses_to_check = 0
            self.current_number_of_addresses_checked = 0
            self.completed_addresses = 0
            CVGTask.__instance = self

    def set_current_id_address_being_checked(self, current_id):
        self.current_id_address_being_checked = current_id

    def increment_current_number_of_addresses_checked(self):
        self.current_number_of_addresses_checked += 1

    def increment_completed_addresses(self):
        self.completed_addresses += 1
        self.write_to_db()

    def write_to_db(self):
        write_to_cvg_task(remark=self.current_id_address_being_checked,
                          total=self.current_number_of_addresses_checked, complete=self.completed_addresses)
