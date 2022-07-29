import mysql.connector
from datetime import datetime
import pytz
from src.singleton.cvg_task import CVGTask
from src.db_read_write.db_secrets import get_db_password
# from db_secrets import get_db_password
from src.singleton.current_input_row import CurrentInputRow
# from current_input_row import CurrentInputRow
from src.db_read_write.db_write_log import write_log_to_db
# from db_write_log import write_log_to_db

from src.notifications.email_msg import send_email
from src.notifications.telegram_msg import send_message
import csv
import time


def write_from_csv_to_db():
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=get_db_password(),
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    # note that 'street_name' and 'street_type' would be put together into 'street'.

    # TODO: double check the create_table statement. result_type should have not null instead of default null. things like these.
    # there ARE 19 columns, however.
    create_table_statement = """
    CREATE TABLE IF NOT EXISTS cvg_db (
        id INT(11) AUTO_INCREMENT PRIMARY KEY,
        unit_no VARCHAR(255) DEFAULT NULL,
        floor VARCHAR(255) DEFAULT NULL,
        building VARCHAR(255) DEFAULT NULL,
        street VARCHAR(255) DEFAULT NULL,
        section VARCHAR(255) DEFAULT NULL,
        city VARCHAR(255) DEFAULT NULL,
        state VARCHAR(255) DEFAULT NULL,
        postcode VARCHAR(255) DEFAULT NULL,
        search_level_flag TINYINT(4) DEFAULT 0,
        source VARCHAR(100) DEFAULT NULL,
        source_id VARCHAR(100) DEFAULT NULL,
        salesman INT(11) DEFAULT NULL,
        notify_email VARCHAR(255) DEFAULT NULL,
        notify_mobile VARCHAR(255) DEFAULT NULL,
        result_type INT(11) DEFAULT NULL,
        result_remark VARCHAR(255) DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );"""

    cursor.execute(create_table_statement)
    cnx.commit()
    cnx.close()
    cursor.close()

    with open('../../second_jaco.csv') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # print(row)
            cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=get_db_password(),
                                          host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
            cursor = cnx.cursor()

            for key, value in row.items():
                if value == '' or value == '-' and 'street' not in key.lower():
                    row[key] = None
                # print(key, value)

            data = (row['\ufeffHouse/Unit/Lot No.'], row['Floor No.'], row['Building Name'], row['Street Type'] + " " + row['Street Name'], row['Section'], row['City'], row['State'], row['Postcode'],
                    row['unit_num_match (0/1)'], row['CUSTOMER EMAIL ADDRESS'], row['CUSTOMER CONTACT NUMBER'])

            insert_statement = """
            INSERT INTO cvg_db ( unit_no, floor, building, street, section, city, state, postcode, search_level_flag, notify_email, notify_mobile )
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
            """

            cursor.execute(insert_statement, data)

            cnx.commit()
            cnx.close()
            cursor.close()


def write_or_edit_result(id, result_type, result_text):
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=get_db_password(),
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    tz = pytz.timezone("Asia/Singapore")
    current_datetime = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    edit_stmt = f"""
    UPDATE cvg_db
    SET result_type = '{result_type}', updated_at = '{current_datetime}', result_remark = '{result_text}'
    WHERE id = {id};
    """
    current_input_row = CurrentInputRow.get_instance()
    # print("RESULTS UPDATED!\n", "id: ", id, "\naddress: ", current_input_row.get_address(self=current_input_row), "\nresult_type: ",
    #   result_type, "\nresult_text: ", result_text)

    cursor.execute(edit_stmt)

    cnx.commit()

    if result_type == 1:
        edit_stmt = f"""
        UPDATE cvg_db
        SET is_active = 0
        WHERE id = {id};
        """
        cursor.execute(edit_stmt)
        cnx.commit()

    cursor.close()
    cnx.close()

    if result_type == 1 or result_type == 2 or result_type == 3:

        current_row_notify_email = current_input_row.get_notify_email(
            self=current_input_row)
        current_row_notify_mobile = current_input_row.get_notify_mobile(
            self=current_input_row)

        if result_type == 1:
            if len(current_row_notify_mobile) > 0:
                send_message(msg="\nIs within serviceable area!")
            if len(current_row_notify_email) > 0:
                send_email(
                    "\nIs within serviceable area!", current_row_notify_email)
        elif result_type == 2:
            if len(current_row_notify_mobile) > 0:
                send_message(
                    msg="\nBuilding Name Found, but Lot Number not Found.")
            if len(current_row_notify_email) > 0:
                send_email(
                    "\nBuilding Name Found, but Lot Number not Found.", current_row_notify_email)
        elif result_type == 3:
            if len(current_row_notify_mobile) > 0:
                send_message(
                    msg="\nStreet Name Found, but Lot Number not Found.")
            if len(current_row_notify_email) > 0:
                send_email(
                    "\nStreet Name Found, but Lot Number not Found.", current_row_notify_email)

    write_log_to_db(id, result_type, result_text)

    # increment the number of addresses checked for cvg_task.
    cvg_task = CVGTask.get_instance()
    cvg_task.increment_completed_addresses()


if __name__ == '__main__':
    write_from_csv_to_db()
# if __name__ == '__main__':
#     for i in range(1, 100):
#         write_or_edit_result(i, 0, "test")
#     write_from_csv_to_db()
