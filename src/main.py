from src.tm_partners.operations.login import Login
from src.tm_partners.singleton.data_id_range import DataIdRange
from src.tm_partners.singleton.cvg_task import CVGTask
from src.tm_partners.singleton.current_db_row import CurrentDBRow
from src.tm_partners.coverage_check.coverage_check import FindingCoverage
from src.tm_partners.singleton.image_names import ImageName
from src.tm_partners.operations.set_accepted_params import set_accepted_params

# TODO: make main an object. so that the singletons are all separate instances for each main object instance.


class Main:
    def __init__(self, thread_name):
        self.thread_name = thread_name

        try:
            image_name = ImageName.get_instance()
            image_name.set_full_page_image_name(
                self=image_name, full_page_image_name=thread_name+"_full_page.png")
            image_name.set_captcha_image_name(
                self=image_name, captcha_image_name=thread_name+"_captcha.png")

            login = Login()
            (driver, a) = login.login()
            finding_coverage = FindingCoverage()
            set_accepted_params()
            # read_from_db()
            finding_coverage.finding_coverage(
                driver=driver, a=a)
            driver.quit()

        except Exception as e:
            print("Some unhandled error occured:", e)

            # check if error is due to site maintenance

            cvg_task = CVGTask.get_instance()
            current_db_row = CurrentDBRow.get_instance()

            # setting the id where error occured
            current_row_id = current_db_row.get_id(
                self=current_db_row)
            if current_row_id is None:
                data_id_range = DataIdRange.get_instance()
                current_row_id = data_id_range.get_start_id(self=data_id_range)
            cvg_task.set_failed_id(self=cvg_task, current_id=current_row_id)
            
            # logging the error
            cvg_task.write_to_db(self=cvg_task)

        # print("Hi! This is a Coverage Automation System. It will:\n1. Read in a Database of Addresses\n2. Check the coverage of the addresses\n3. Send an email with a screenshot depending on the 4 coverage end results.")
        # ids_to_start_from = input(
        #     "What id-s would you like to start from? (Press ENTER to check all.)")
        # ids_to_end_at = input(
        #     "Now please enter the id to end at. (Press ENTER to check all.)")

        # if ids_to_start_from == '':
        #     ids_to_start_from = 1
        # if ids_to_end_at == '':
        #     ids_to_end_at = -1

    # TODO: skip the database addresses that are already noted as covered.
    # TODO: when searching for 'condominium' in address, if no results, search for 'kondominium'
    # TODO: created_at, updated_at in the database
    # TODO: do 'no result' for when there are no results in the TABLE screen.

    # seven scenarios:
    # id 1. within servicable areas (Available)
    # id 2. Building Name Found
    # id 3. Street Name Found
    # id 4: Not within Serviceable Area
    # id 5: service provider not the same with Transfer Request,
    # id 6: Another progressing order created on the same address has been detected (Existing Order).
    # id 7: Port full.
    # id 8: No results in the results table.

    # 3. outside servicable areas,
    # for when the flag to  be detailed to lot no is NO.
    # scenario is used for when new AREAS are added into unifi database.
    # 3a.
    # first, search for the specific lot no. if no results are returned, then search for the building name.
    # Since the flag to get more details is set to NO,
    # 3b.
    # first, search for the specific lot no. if no results are returned, then search for the street name.
    # Since the flag to get more details is set to NO,
    # 5.

    # the file of the csv is in coverage check.py, line 283.

    # four address examples:
    # 1. within servicable areas (No. A-1-8, Floor 1, DATARAN EMARALD Building, JALAN PS 11 Section PRIMA SELAYANG, 68100 BATU CAVES SELANGOR, MALAYSIA)
    # 2. service provider not the same with Transfer Request (No. 12, Floor -, JALAN DAGANG JAYA, 68000 AMPAND SELANGOR, MALAYSIA)
    # 3. outside servicable areas (No. C4-6-2, Floor 6, FTTH EVERGREEN PARK CYPRESS CONDOMINIUM BLOK C4 BUilding. PERSIARAN SUNGAI LONG 1 Section BANDAR SUNGAI LONG, 43000 KALANG SELANGOR, MALAYSIA)
    # 4. Another progressing order created on the same address has been detected (No. 38, JALAN SS 26/7 Section TAMAN MAYANG JAYA, 47301 PETALING JAYA SELANGOR, MALAYSIA)

    # analysis on the xpath for the table results:
    # when there's only one result (without using the filter boxes to filter), the xpath for the tr @class is "[@class='datagrid-even']"
    # when there's multiple results (without using the filter boxes to filter), the xpath for the tr @class is "[@class='odd' or @class='even']"
    # after you filter using the filter box, the xpath would be //tr[@class='odd' or @class='even'][not(@style)]


# if __name__ == '__main__':
#     Main.main()
