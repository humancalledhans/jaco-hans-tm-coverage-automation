
from src.tm_global.singleton.cvg_task import CVGTask
from src.tm_global.singleton.current_db_row import CurrentDBRow


def set_cvg_task():
    cvg_task = CVGTask.get_instance()
    current_row_id = CurrentDBRow.get_instance().get_id()
    cvg_task.set_current_id_address_being_checked(
        current_id=current_row_id)
    cvg_task.increment_current_number_of_addresses_checked()

    # cvg_task needs to be such that:
    # 1. it needs to write the total amount of addresses that are supposed to be checked.
    # 2. it needs to write the actual number of addresses that have been checked.
    # 3. it needs to write the id that the code has stopped at.
    # - for 3, it would be an exception that cannot be handled.

    # maybe cvg_task should be a Singleton!!
    # - it would have one for every whole run of the code.
    # - we would write once to the database, at the end.
