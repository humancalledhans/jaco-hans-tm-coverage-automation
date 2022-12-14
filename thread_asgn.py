import threading
from src.tm_partners.singleton.num_of_iterations import NumOfIterations
from src.tm_partners.singleton.data_id_range import DataIdRange
from src.tm_partners.db_read_write.db_get_largest_id import get_max_id_from_db
from src.tm_partners.db_read_write.db_get_smallest_id import get_min_id_from_db

from src.main import Main
from src.tm_partners.operations.retry_problematic_ids import retry_problematic_ids


class ThreadAsgn:
    def __init__(self, ids_to_start_from=get_min_id_from_db(), ids_to_end_at=get_max_id_from_db()):
    # def __init__(self, ids_to_start_from=1251, ids_to_end_at=1251):
        self.ids_to_start_from = ids_to_start_from
        self.ids_to_end_at = ids_to_end_at
        data_id_range = DataIdRange.get_instance()
        data_id_range.set_start_id(
            self=data_id_range, start_id=int(ids_to_start_from))
        data_id_range.set_end_id(self=data_id_range,
                                 end_id=int(ids_to_end_at))

    def main_thread(self, thread_name):
        # get the indexes, and then assign the indexes to four different threads
        Main(thread_name)
        retry_problematic_ids(thread_name)

    def start_threads(self):

        # print("START", full_ids_to_start)
        # print("END", full_ids_to_end)

        threading.Thread(target=self.main_thread,
                         args=("thread-1",)).start()

        # if full_ids_to_end - full_ids_to_start < 4:
        #     threading.Thread(target=self.main_thread, args=(
        #         full_ids_to_start, full_ids_to_end, "thread-1")).start()

        # elif (full_ids_to_end - full_ids_to_start) % 4 == 0:
        #     threading.Thread(target=self.main_thread, args=(
        #         full_ids_to_start, full_ids_to_start + int(full_ids_to_end / 4), "thread-1")).start()
        #     threading.Thread(target=self.main_thread, args=(
        #         full_ids_to_start + int(full_ids_to_end / 4), full_ids_to_start + int(full_ids_to_end / 2), "thread-2")).start()
        #     threading.Thread(target=self.main_thread, args=(
        #         full_ids_to_start + int(full_ids_to_end / 2), full_ids_to_start + int(full_ids_to_end * 3 / 4), "thread-3")).start()
        #     threading.Thread(target=self.main_thread, args=(
        #         full_ids_to_start + int(full_ids_to_end * 3 / 4), full_ids_to_end, "thread-4")).start()

        # elif (full_ids_to_end - full_ids_to_start) % 3 == 0:
        #     threading.Thread(target=self.main_thread, args=(
        #         full_ids_to_start, full_ids_to_start + int(full_ids_to_end / 3), "thread-1")).start()
        #     threading.Thread(target=self.main_thread, args=(
        #         full_ids_to_start + int(full_ids_to_end / 3), full_ids_to_start + int(full_ids_to_end * 2 / 3), "thread-2")).start()
        #     threading.Thread(target=self.main_thread, args=(
        #         full_ids_to_start + int(full_ids_to_end * 2 / 3), full_ids_to_end, "thread-3")).start()

        # elif (full_ids_to_end - full_ids_to_start) % 2 == 0:
        #     threading.Thread(target=self.main_thread, args=(
        #         full_ids_to_start, full_ids_to_start + int(full_ids_to_e`nd / 2), "thread-1")).start()
        #     threading.Thread(target=self.main_thread, args=(
        #         full_ids_to_start + int(full_ids_to_end / 2), full_ids_to_end, "thread-2")).start()


if __name__ == '__main__':
    num_of_iterations = 1  # jaco, change this line.
    num_of_iterations_instance = NumOfIterations.get_instance()
    num_of_iterations_instance.set_num_of_iterations(int(num_of_iterations))
    thread_asgn = ThreadAsgn(1374, 1374)
    thread_asgn.start_threads()

    # x = threading.Thread(target=func)
    # x.start()
    # print(threading.activeCount())
