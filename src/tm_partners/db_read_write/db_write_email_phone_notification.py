from asyncore import write
import mysql.connector
from datetime import datetime
from src.tm_partners.db_read_write.db_secrets import get_db_password
# from db_secrets import get_db_password


def write_from_csv_to_db(start=0, end=0):
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=get_db_password(),
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")

    cursor = cnx.cursor()

    for id in range(start, end+1):
        enter_log = f"""
        UPDATE cvg_db
        SET notify_email = 'hansworktests@gmail.com', notify_mobile = '60165239321'
        WHERE id = {id};
        """

        cursor.execute(enter_log)

        cnx.commit()

    cursor.close()
    cnx.close()


if __name__ == '__main__':
    write_from_csv_to_db(1, 62)
