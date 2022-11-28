from datetime import datetime
import smtplib
import time

from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.tm_global.singleton.current_db_row import CurrentDBRow


def setup_notification_text(text):
    current_db_row = CurrentDBRow.get_instance()
    email_text = f"""
Current Date Time: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

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

{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} End of message.
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
    # print('send email method called')
    # print("EMAIL_TO................", email_to)
    gmail_user = 'botourssp@gmail.com'
    gmail_password = 'jshmktlmwgeginnx'
    current_db_row = CurrentDBRow.get_instance()
    content = setup_notification_text(text)

    if len(email_to) > 0:
        email_to_list = email_to.split(',')

        for email in email_to_list:
            email_to = email.strip()
            # email_to = 'hansmaildump@gmail.com'
            # subject = 'Coverage Automation Notification'
            print("CURRENT ID", current_db_row.get_id(self=current_db_row))
            subject = f'ACC TID {current_db_row.get_id(self=current_db_row)}'
            body = EmailMessage()
            body2 = EmailMessage()
            body.set_content(content)
            body.set_default_type("text/html")

            # print("SENDING MESSAGE...")
            try:

                # smtp_server.ehlo()
                # smtp_server.sendmail(sent_from, to, body)
                # smtp_server.close()
                body['Subject'] = subject
                body['From'] = gmail_user
                body['To'] = email_to
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp_server.login(gmail_user, gmail_password)
                smtp_server.send_message(body)
                smtp_server.quit()
            except Exception as ex:
                # break
                print(ex)


if __name__ == '__main__':
    send_email()
