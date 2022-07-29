import threading
from src.main import Main

from src.db_read_write.db_get_largest_id import get_max_id_from_db


class ThreadAsgn:
    def __init__(self, ids_to_start_from=1, ids_to_end_at=get_max_id_from_db()):
        self.ids_to_start_from = ids_to_start_from
        self.ids_to_end_at = ids_to_end_at

    def main_thread(self, id_to_start, id_to_end, thread_name):
        # get the indexes, and then assign the indexes to four different threads
        Main(id_to_start, id_to_end, thread_name)

    def start_threads(self):
        full_ids_to_start = self.ids_to_start_from
        full_ids_to_end = self.ids_to_end_at

        threading.Thread(target=self.main_thread, args=(
            full_ids_to_start, full_ids_to_end, "thread-1")).start()

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
    # def func():
    #     print('ran')
    #     time.sleep(1)
    #     print('done')
    #     time.sleep(0.85)
    #     print('now done')

    # x = threading.Thread(target=func)
    # x.start()
    # print(threading.activeCount())
    # time.sleep(0.9)
    # print('finally')
    thread_asgn = ThreadAsgn()
    thread_asgn.start_threads()
