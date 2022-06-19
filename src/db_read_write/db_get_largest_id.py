import mysql.connector


def get_max_id_from_db():
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password="ExtInfo!@#",
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    query = f"SELECT * FROM cvg_db ORDER BY id DESC LIMIT 0,1"
    cursor.execute(query)
    result = cursor.fetchall()

    current_row = result[0]

    return current_row[0]
