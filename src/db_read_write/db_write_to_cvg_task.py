import mysql.connector
from datetime import datetime

import pytz
from src.db_read_write.db_secrets import get_db_password


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
