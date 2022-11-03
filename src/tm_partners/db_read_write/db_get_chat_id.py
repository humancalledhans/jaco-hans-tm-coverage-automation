import mysql.connector

from src.tm_partners.db_read_write.db_secrets import get_db_password
# from db_secrets import get_db_password


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


if __name__ == '__main__':
    print(get_chat_id("60165239321"))
