import smtplib
import time

from src.singleton.current_input_row import CurrentInputRow


def setup_notification_text(text):
    current_input_row = CurrentInputRow.get_instance()
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
	""" % (current_input_row.get_id(self=current_input_row), current_input_row.get_source(self=current_input_row),
        current_input_row.get_source_id(
            self=current_input_row), current_input_row.get_house_unit_lotno(self=current_input_row),
        current_input_row.get_street(
            self=current_input_row), current_input_row.get_section(self=current_input_row),
        current_input_row.get_floor(
            self=current_input_row), current_input_row.get_building(self=current_input_row),
        current_input_row.get_city(
            self=current_input_row), current_input_row.get_state(self=current_input_row),
        current_input_row.get_postcode(self=current_input_row), text)

    return email_text


def send_email(text, email_to):
    gmail_user = 'botourssp@gmail.com'
    gmail_password = 'jshmktlmwgeginnx'

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
            print("Something went wrong….", ex)


if __name__ == '__main__':
    send_email()
