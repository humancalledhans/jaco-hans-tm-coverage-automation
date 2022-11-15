import smtplib
import mysql.connector
import requests

from src.tm_global.db_read_write.db_secrets import get_db_password
from src.tm_global.singleton.current_db_row import CurrentDBRow


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
    address_string = current_db_row.get_address(self=current_db_row)

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
