import mysql.connector
from datetime import datetime
from src.db_read_write.db_secrets import get_db_password


def write_to_cvg_task(remark, total, complete):
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=get_db_password(),
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    current_time = datetime.now()

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

    values = (remark, total, complete, current_time, current_time)

    cursor.execute(enter_log, values)

    cnx.commit()

    cursor.close()
    cnx.close()
