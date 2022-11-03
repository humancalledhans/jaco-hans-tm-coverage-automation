import mysql.connector

from src.tm_global.db_read_write.db_secrets import get_db_password


def get_max_id_from_db():
    password = get_db_password()
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=password,
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    query = f"SELECT * FROM cvg_db ORDER BY id DESC LIMIT 0,1"
    cursor.execute(query)
    result = cursor.fetchall()

    return result[0][0]
