import mysql.connector
from datetime import datetime

import pytz
from src.tm_global.db_read_write.db_secrets import get_db_password
from src.tm_global.singleton.selected_table_row import SelectedTableRow
from src.tm_global.singleton.current_db_row import CurrentDBRow
from src.tm_global.notifications.email_msg import send_email
from src.tm_global.notifications.telegram_msg import send_message


def write_results_to_db():
    selected_table_row_instance = SelectedTableRow.get_instance()
    address_remark = selected_table_row_instance.get_address(
        self=selected_table_row_instance).replace("\'", "\\'")

    current_db_row_instance = CurrentDBRow.get_instance()

    id = current_db_row_instance.get_id(self=current_db_row_instance)
    result_remark = selected_table_row_instance.get_result_remark(
        self=selected_table_row_instance)

    filters_used_list_form = selected_table_row_instance.get_filters_used_to_search(
        self=selected_table_row_instance)
    filters_used = ""
    for filter_idx in range(len(filters_used_list_form)):
        if filter_idx == len(filters_used_list_form) - 1:
            filters_used += filters_used_list_form[filter_idx]
        else:
            filters_used += filters_used_list_form[filter_idx] + ", "

    print("ID: ", id)
    print("RESULT REMARK: ", result_remark)
    print("ADDRESS REMARK: ", address_remark + "\n")
    print("CURRENT DB ADDRESS ", current_db_row_instance.get_address(
        self=current_db_row_instance))
    print("part of address used to search: ", selected_table_row_instance.get_part_of_address_used(
        self=selected_table_row_instance))
    print("filters successfully used for search",
          selected_table_row_instance.get_filters_used_to_search(self=selected_table_row_instance))

    print("\n* * * * * * * * * * * *\n")

    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=get_db_password(),
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    tz = pytz.timezone("Asia/Singapore")
    current_datetime = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    # edit_stmt = f"""
    # UPDATE cvg_db
    # SET result_type_global = '{result_type}', updated_at_global = '{current_datetime}', result_remark_global = '{result_remark}'
    # WHERE id = {id};
    # """

    edit_stmt = f"""
    UPDATE cvg_db
    SET updated_at_global = '{current_datetime}', result_remark_global = '{result_remark}', address_used_global = '{address_remark}', filters_used_global = '{filters_used}'
    WHERE id = {id};
    """
    # print("RESULTS UPDATED!\n", "id: ", id, "\naddress: ", current_db_row.get_address(self=current_db_row), "\nresult_type: ",
    #   result_type, "\nresult_text: ", result_text)

    cursor.execute(edit_stmt)

    cnx.commit()

    # # if result_type == 1:
    # #     edit_stmt = f"""
    # #     UPDATE cvg_db
    # #     SET is_active = 0
    # #     WHERE id = {id};
    # #     """
    # #     cursor.execute(edit_stmt)
    # #     cnx.commit()

    cursor.close()
    cnx.close()

    if result_remark == 'Within Serviceable Area.':
        current_row_notify_email = current_db_row_instance.get_notify_email(
            self=current_db_row_instance)
        current_row_notify_mobile = current_db_row_instance.get_notify_mobile(
            self=current_db_row_instance)

        if current_row_notify_mobile is not None and current_row_notify_mobile.lower() != "null":
            if len(current_row_notify_mobile) > 0:
                send_message(msg="\nIs within serviceable area!")
        if current_row_notify_email is not None and current_row_notify_email.lower() != "null":
            if len(current_row_notify_email) > 0:
                send_email(
                    "\nIs within serviceable area!", current_row_notify_email)

    elif result_remark == 'Within Servicable Area, Require New Infra Development':
        current_row_notify_email = current_db_row_instance.get_notify_email(
            self=current_db_row_instance)
        current_row_notify_mobile = current_db_row_instance.get_notify_mobile(
            self=current_db_row_instance)

        if current_row_notify_mobile is not None and current_row_notify_mobile.lower() != "null":
            if len(current_row_notify_mobile) > 0:
                send_message(
                    msg="\nWithin serviceable area, require New Infra development")
        if current_row_notify_email is not None and current_row_notify_email.lower() != "null":
            if len(current_row_notify_email) > 0:
                send_email(
                    "\nWithin serviceable area, require New Infra development", current_row_notify_email)

    # if result_type == 1 or result_type == 2 or result_type == 3:

    #     current_row_notify_email = current_db_row.get_notify_email(
    #         self=current_db_row)
    #     current_row_notify_mobile = current_db_row.get_notify_mobile(
    #         self=current_db_row)

    #     # print("CURRENT ROW EMAIL", current_row_notify_email)
    #     # print("CURRENT ROW MOBILE", current_row_notify_mobile)

    #     if result_type == 1:
    #         if current_row_notify_mobile is not None and current_row_notify_mobile.lower() != "null":
    #             if len(current_row_notify_mobile) > 0:
    #                 send_message(msg="\nIs within serviceable area!")
    #         if current_row_notify_email is not None and current_row_notify_email.lower() != "null":
    #             if len(current_row_notify_email) > 0:
    #                 send_email(
    #                     "\nIs within serviceable area!", current_row_notify_email)
    #     elif result_type == 2:
    #         if current_row_notify_mobile is not None and current_row_notify_mobile.lower() != "null":
    #             if len(current_row_notify_mobile) > 0:
    #                 send_message(
    #                     msg="\nBuilding Name Found, but Lot Number not Found.")
    #         if current_row_notify_email is not None and current_row_notify_email.lower() != "null":
    #             if len(current_row_notify_email) > 0:
    #                 send_email(
    #                     "\nBuilding Name Found, but Lot Number not Found.", current_row_notify_email)
    #     elif result_type == 3:
    #         if current_row_notify_mobile is not None and current_row_notify_mobile.lower() != "null":
    #             if len(current_row_notify_mobile) > 0:
    #                 send_message(
    #                     msg="\nStreet Name Found, but Lot Number not Found.")
    #         if current_row_notify_email is not None and current_row_notify_email.lower() != "null":
    #             if len(current_row_notify_email) > 0:
    #                 send_email(
    #                     "\nStreet Name Found, but Lot Number not Found.", current_row_notify_email)

    # write_log_to_db(id, result_type, result_text, address_remark)

    # # increment the number of addresses checked for cvg_task.
    # cvg_task = CVGTask.get_instance()
    # cvg_task.increment_total_number_of_addresses_checked()
