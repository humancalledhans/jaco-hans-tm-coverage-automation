import mysql.connector
import pandas as pd


def upload_to_db():
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password="ExtInfo!@#",
                                  host="103.6.198.226", port='3306', database="oursspc1_db_coverage")
    cursor = cnx.cursor()

    # columns = ("id", "unit_no", "floor", "building", "street", "section",
    #            "city", "state", "postcode", "created_at", "updated_at")

    create_table_statement = """
    CREATE TABLE IF NOT EXISTS cvg_db_by_hans (
        id INT(11) AUTO_INCREMENT PRIMARY KEY,
        house_no VARCHAR(255),
        floor INT,
        street_name VARCHAR(255),
        section VARCHAR(255),
        building VARCHAR(255),
        city VARCHAR(255),
        state VARCHAR(255),
        postcode VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );"""

    cursor.execute(create_table_statement)

    df = pd.read_csv('Port full_or_Coming soon.csv')
    df.to_sql('port_full_or_Coming_soon', cnx, if_exists='append', index=False)

    # create_table_statement = """
    # CREATE TABLE IF NOT EXISTS cvg_db_by_hans (
    #     id INT(11) AUTO_INCREMENT PRIMARY KEY,
    #     house_no VARCHAR(255),
    #     floor INT,
    #     street_name VARCHAR(255),
    #     section VARCHAR(255),
    #     building VARCHAR(255),
    #     city VARCHAR(255),
    #     state VARCHAR(255),
    #     postcode VARCHAR(255),
    #     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    # );"""

    # date = {'house_no': "LOT 1640"}
    # values = ()
    # cursor.execute(create_table_statement)


if __name__ == '__main__':
    upload_to_db()
