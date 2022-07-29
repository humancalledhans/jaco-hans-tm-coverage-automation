import mysql.connector
from datetime import datetime
from src.db_read_write.db_secrets import get_db_password
# from db_secrets import get_db_password


def write_log_to_db(db_id, result_type, result_remark):
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=get_db_password(),
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    current_time = datetime.now()

    create_table_statement = """
    CREATE TABLE IF NOT EXISTS cvg_log (
        db_id INT(11),
        result_type INT(11),
        result_remark VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

    # enter_log = f"""
    # UPDATE cvg_log
    # SET result_type = '{result_type}', result_remark = '{result_remark}', created_at = '{current_time}'
    # WHERE db_id = {db_id};
    # """

    enter_log = """
    INSERT INTO cvg_log (db_id, result_type, result_remark, created_at)
    VALUES (%s, %s, %s, %s)
    """

    values = (db_id, result_type, result_remark, current_time)

    # cursor.execute(create_table_statement)
    cursor.execute(enter_log, values)

    cnx.commit()

    cursor.close()
    cnx.close()


if __name__ == '__main__':
    write_log_to_db(1, 2, 'test')
