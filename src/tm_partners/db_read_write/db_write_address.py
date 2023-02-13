from abc import ABCMeta, abstractstaticmethod
import mysql.connector
from datetime import datetime
import smtplib
import pytz
import requests

import csv
import time

from src.tm_partners.singleton.current_db_row import CurrentDBRow
from src.tm_partners.singleton.cvg_task import CVGTask
from src.tm_partners.singleton.selected_table_row import SelectedTableRow


def get_chat_id(desired_phone_number):
    password = get_db_password()
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=password,
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    query = "SELECT chat_id FROM cvg_telegram WHERE phone_no = %s"
    phone_num_tuple = (desired_phone_number,)
    cursor.execute(query, phone_num_tuple)
    result = cursor.fetchall()

    result = result[0][0]
    return result


def send_message(msg):
    current_db_row = CurrentDBRow.get_instance()
    phone_num_list = current_db_row.get_notify_mobile(
        self=current_db_row).split(',')

    # to take away same phone numbers in a list.
    phone_num_list = list(set(phone_num_list))

    try:
        helper_send_message(msg, phone_num_list=phone_num_list)
    except Exception as ex:
        print(ex)


def helper_send_message(msg, phone_num_list):

    TOKEN = "5558294620:AAGKJDU0ja0ys_0T2-4JhVGx-3XJ1zJRtow"
    # text = "JacoHansCABot speaks"
    address_string = ''
    current_db_row = CurrentDBRow.get_instance()
    input_house_unit_lotno = current_db_row.get_house_unit_lotno(
        self=current_db_row)
    input_street = current_db_row.get_street(
        self=current_db_row)
    input_section = current_db_row.get_section(
        self=current_db_row)
    input_floor_no = current_db_row.get_floor(
        self=current_db_row)
    input_building_name = current_db_row.get_building(
        self=current_db_row)
    input_city = current_db_row.get_city(self=current_db_row)
    input_state = current_db_row.get_state(
        self=current_db_row)
    input_postcode = current_db_row.get_postcode(
        self=current_db_row)

    if input_house_unit_lotno is None:
        input_house_unit_lotno = ''
    if input_street is None:
        input_street = ''
    if input_section is None:
        input_section = ''
    if input_floor_no is None:
        input_floor_no = ''
    if input_building_name is None:
        input_building_name = ''
    if input_city is None:
        input_city = ''
    if input_state is None:
        input_state = ''
    if input_postcode is None:
        input_postcode = ''

    address_string = address_string + \
        "House/Unit/Lot No." + input_house_unit_lotno + '\n' + \
        "Street: " + input_street + '\n' + \
        "Section: " + input_section + '\n' + \
        "Floor No: " + input_floor_no + '\n' + \
        "Building Name: " + input_building_name + '\n' + \
        "City: " + input_city + '\n' + \
        "State: " + input_state + '\n' + \
        "Postcode: " + input_postcode

    for elem in phone_num_list:
        # for every phone number.
        try:
            chat_id = get_chat_id(elem.strip())

            text = address_string + msg
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
            # url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            r = requests.get(url)

        except IndexError:
            current_row_id = current_db_row.get_id(self=current_db_row)
            raise Exception(f"No chat id found for row id {current_row_id}")


def setup_notification_text(text):
    current_db_row = CurrentDBRow.get_instance()
    email_text = """
Id: %s
Source: %s
Source Trx id: %s
Unit: %s
Street: %s
Section: %s
Floor No: %s
Building Name: %s
City: %s
State: %s
Postcode: %s
    %s
	""" % (current_db_row.get_id(self=current_db_row), current_db_row.get_source(self=current_db_row),
        current_db_row.get_source_id(
            self=current_db_row), current_db_row.get_house_unit_lotno(self=current_db_row),
        current_db_row.get_street(
            self=current_db_row), current_db_row.get_section(self=current_db_row),
        current_db_row.get_floor(
            self=current_db_row), current_db_row.get_building(self=current_db_row),
        current_db_row.get_city(
            self=current_db_row), current_db_row.get_state(self=current_db_row),
        current_db_row.get_postcode(self=current_db_row), text)

    return email_text


def send_email(text, email_to):
    selected_table_row_instance = SelectedTableRow.get_instance()

    address_chosen = selected_table_row_instance.get_address(
        self=selected_table_row_instance).replace(
        "  ", " ").replace("   ", " ")

    current_db_row = CurrentDBRow.get_instance()
    address_from_db = current_db_row.get_address_with_headers(self=current_db_row).replace(
        "  ", " ").replace("   ", " ")

    gmail_user = 'botourssp@gmail.com'
    gmail_password = 'jshmktlmwgeginnx'

    if len(email_to) > 0:
        email_to_list = email_to.split(',')

        for email in email_to_list:
            email_to = email.strip()
            sent_from = gmail_user
            to = email_to
            subject = 'Coverage Automation Notification'
            body = setup_notification_text(text)

            try:
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp_server.ehlo()
                smtp_server.login(gmail_user, gmail_password)
                smtp_server.sendmail(sent_from, to, body)
                smtp_server.close()
            except Exception as ex:
                break


def get_db_password():
    return "ExtInfo!@#"


def write_log_to_db(db_id, result_type, result_remark, address_remark=None):
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=get_db_password(),
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    tz = pytz.timezone("Asia/Singapore")
    current_datetime = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    create_table_statement = """
    CREATE TABLE IF NOT EXISTS cvg_log (
        db_id INT(11),
        result_type INT(11),
        result_remark VARCHAR(255),
        created_at TIMESTAMP,
        address_remark VARCHAR(255),
        )
    """

    # enter_log = f"""
    # UPDATE cvg_log
    # SET result_type = '{result_type}', result_remark = '{result_remark}', created_at = '{current_time}'
    # WHERE db_id = {db_id};
    # """

    enter_log = """
    INSERT INTO cvg_log (db_id, result_type, result_remark, created_at, address_remark)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (db_id, result_type, result_remark,
              current_datetime, address_remark)

    # cursor.execute(create_table_statement)
    cursor.execute(enter_log, values)

    cnx.commit()

    cursor.close()
    cnx.close()


def write_to_cvg_task(remark, total, complete):
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=get_db_password(),
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    tz = pytz.timezone("Asia/Singapore")
    current_datetime = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    create_table_statement = """
    CREATE TABLE IF NOT EXISTS cvg_task (
        id INT PRIMARY_KEY AUTO_INCREMENT,
        remark VARCHAR(255),
        total INT,
        complete INT,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
        )
    """

    # remark = current id of address being checked
    # total = total number of addresses to check
    # complete = current number of addresses checked

    enter_log = """
    INSERT INTO cvg_task (remark, total, complete, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (remark, total, complete, current_datetime, current_datetime)

    cursor.execute(enter_log, values)

    cnx.commit()

    cursor.close()
    cnx.close()


def write_from_csv_to_db():
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=get_db_password(),
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    # note that 'street_name' and 'street_type' would be put together into 'street'.
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
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    );"""

    tz = pytz.timezone("Asia/Singapore")
    current_datetime = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

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
                    row['unit_num_match (0/1)'], row['CUSTOMER EMAIL ADDRESS'], row['CUSTOMER CONTACT NUMBER'], current_datetime)

            insert_statement = """
            INSERT INTO cvg_db ( unit_no, floor, building, street, section, city, state, postcode, search_level_flag, notify_email, notify_mobile, created_at )
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
            """

            cursor.execute(insert_statement, data)

            cnx.commit()
            cnx.close()
            cursor.close()

# class InvalidSingletonError(Exception):
#     """Custom exception raised for errors with singleton declarations

#     Args:
#         message (str): the message to be displayed
#     """
#     def __init__(self, message="A singleton instance seems to be problematic."):
#         self.message = message
#         super().__init__(self.message)

def write_or_edit_result(id, result_type, result_text):

    selected_table_row_instance = SelectedTableRow.get_instance()
    current_db_row_instance = CurrentDBRow.get_instance()

    address_remark = selected_table_row_instance.get_address(
        self=selected_table_row_instance)

    
    # enforcing the table row address to exist if result exists
    is_address_expected = result_type != 8 and result_type != 2 and result_type != 3
    if is_address_expected and len(address_remark) == 0:
        raise ValueError("SelectedTableRow instance is expected to be set!")

    # adding the common parts of the address to address_remark
    overlapping_tokens = ''
    if len(address_remark) != 0:

        selected_table_row_unit = selected_table_row_instance.get_unit_no(
            self=selected_table_row_instance)
        current_db_row_unit = current_db_row_instance.get_house_unit_lotno(
            self=current_db_row_instance)
        if selected_table_row_unit == current_db_row_unit:
            overlapping_tokens += current_db_row_unit

        selected_table_row_floor = selected_table_row_instance.get_floor(
            self=selected_table_row_instance)
        current_db_row_floor = current_db_row_instance.get_floor(
            self=current_db_row_instance)
        if selected_table_row_floor == current_db_row_floor:
            overlapping_tokens += ' ' + current_db_row_floor

        selected_table_row_building = selected_table_row_instance.get_building(
            self=selected_table_row_instance)
        current_db_row_building = current_db_row_instance.get_building(
            self=current_db_row_instance)
        if selected_table_row_building == current_db_row_building:
            overlapping_tokens += ' ' + current_db_row_building

        try:
            selected_table_row_street = selected_table_row_instance.get_street_type(
                self=selected_table_row_instance) + ' ' + selected_table_row_instance.get_street_name(self=selected_table_row_instance)
        except:
            selected_table_row_street = selected_table_row_instance.get_street_type(
                self=selected_table_row_instance)
        current_db_row_street = current_db_row_instance.get_street(
            self=current_db_row_instance)
        if selected_table_row_street == current_db_row_street:
            overlapping_tokens += ' ' + current_db_row_street

        selected_table_row_section = selected_table_row_instance.get_section(
            self=selected_table_row_instance)
        current_db_row_section = current_db_row_instance.get_section(
            self=current_db_row_instance)
        if selected_table_row_section == current_db_row_section:
            overlapping_tokens += ' ' + current_db_row_section

        selected_table_row_city = selected_table_row_instance.get_city(
            self=selected_table_row_instance)
        current_db_row_city = current_db_row_instance.get_city(
            self=current_db_row_instance)
        if selected_table_row_city == current_db_row_city:
            overlapping_tokens += ' ' + current_db_row_city

        selected_table_row_state = selected_table_row_instance.get_state(
            self=selected_table_row_instance)
        current_db_row_state = current_db_row_instance.get_state(
            self=current_db_row_instance)
        if selected_table_row_state == current_db_row_state:
            overlapping_tokens += ' ' + current_db_row_state

        selected_table_row_postcode = selected_table_row_instance.get_postcode(
            self=selected_table_row_instance)
        current_db_row_postcode = current_db_row_instance.get_postcode(
            self=current_db_row_instance)
        if selected_table_row_postcode == current_db_row_postcode:
            overlapping_tokens += ' ' + current_db_row_postcode

        overlapping_tokens = overlapping_tokens.strip().strip()

    print("ID: ", id)
    print("RESULT TYPE: ", result_type)
    print("RESULT TEXT: ", result_text)
    print("ADDRESS REMARK: ", address_remark)
    print("------------")
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=get_db_password(),
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    tz = pytz.timezone("Asia/Singapore")
    current_datetime = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    edit_stmt = f"""
    UPDATE cvg_db
    SET result_type = '{result_type}', updated_at = '{current_datetime}', result_remark = '{result_text}', address_used_tm_partners = '{address_remark}'
    WHERE id = {id};
    """
    current_db_row = CurrentDBRow.get_instance()
    # print("RESULTS UPDATED!\n", "id: ", id, "\naddress: ", current_db_row.get_address(self=current_db_row), "\nresult_type: ",
    #   result_type, "\nresult_text: ", result_text)

    cursor.execute(edit_stmt)

    cnx.commit()

    # if result_type == 1:
    #     edit_stmt = f"""
    #     UPDATE cvg_db
    #     SET is_active = 0
    #     WHERE id = {id};
    #     """
    #     cursor.execute(edit_stmt)
    #     cnx.commit()

    cursor.close()
    cnx.close()

    if result_type == 1 or result_type == 2 or result_type == 3:

        current_row_notify_email = current_db_row.get_notify_email(
            self=current_db_row)
        current_row_notify_mobile = current_db_row.get_notify_mobile(
            self=current_db_row)

        # print("CURRENT ROW EMAIL", current_row_notify_email)
        # print("CURRENT ROW MOBILE", current_row_notify_mobile)

        if result_type == 1:
            if current_row_notify_mobile is not None and current_row_notify_mobile.lower() != "null":
                if len(current_row_notify_mobile) > 0:
                    send_message(msg="\nIs within serviceable area!")
            if current_row_notify_email is not None and current_row_notify_email.lower() != "null":
                if len(current_row_notify_email) > 0:
                    send_email(
                        "\nIs within serviceable area!", current_row_notify_email)
        elif result_type == 2:
            if current_row_notify_mobile is not None and current_row_notify_mobile.lower() != "null":
                if len(current_row_notify_mobile) > 0:
                    send_message(
                        msg="\nBuilding Name Found, but Lot Number not Found.")
            if current_row_notify_email is not None and current_row_notify_email.lower() != "null":
                if len(current_row_notify_email) > 0:
                    send_email(
                        "\nBuilding Name Found, but Lot Number not Found.", current_row_notify_email)
        elif result_type == 3:
            if current_row_notify_mobile is not None and current_row_notify_mobile.lower() != "null":
                if len(current_row_notify_mobile) > 0:
                    send_message(
                        msg="\nStreet Name Found, but Lot Number not Found.")
            if current_row_notify_email is not None and current_row_notify_email.lower() != "null":
                if len(current_row_notify_email) > 0:
                    send_email(
                        "\nStreet Name Found, but Lot Number not Found.", current_row_notify_email)

    write_log_to_db(id, result_type, result_text, address_remark)

    # increment the number of addresses checked for cvg_task.
    cvg_task = CVGTask.get_instance()
    cvg_task.increment_total_number_of_addresses_checked(self=cvg_task)


if __name__ == '__main__':
    write_from_csv_to_db()
# if __name__ == '__main__':
#     for i in range(1, 100):
#         write_or_edit_result(i, 0, "test")
#     write_from_csv_to_db()
