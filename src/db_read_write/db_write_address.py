import mysql.connector
import pandas as pd
import csv


def upload_to_db():
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password="ExtInfo!@#",
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    # columns = ("id", "unit_no", "floor", "building", "street", "section",
    #            "city", "state", "postcode", "created_at", "updated_at")

    # 'street_name' and 'street_type' would be put together into 'street'.

    # TODO: double check the create_table statement. result_type should have not null instead of default null. things like these.
    # there ARE 19 columns, however.
    create_table_statement = """
    CREATE TABLE IF NOT EXISTS cvg_db (
        id INT(11) AUTO_INCREMENT PRIMARY KEY,
        unit_no VARCHAR(255) DEFAULT NULL,
        floor VARCHAR(255) DEFAULT NULL,
        building VARCHAR(255) DEFAULT NULL,
        street VARCHAR(255) DEFAULT NULL, 
        section VARCHAR(255) DEFAULT NULL,
        city VARCHAR(255) DEFAULT NULL,
        state VARCHAR(255) DEFAULT NULL,
        postcode VARCHAR(255) DEFAULT NULL,
        search_level_flag TINYINT(4) DEFAULT 0,
        source VARCHAR(100) DEFAULT NULL,
        source_id VARCHAR(100) DEFAULT NULL,
        salesman INT(11) DEFAULT NULL,
        notify_email VARCHAR(255) DEFAULT NULL,
        notify_mobile VARCHAR(255) DEFAULT NULL,
        result_type INT(11) DEFAULT NULL,
        result_remark VARCHAR(255) DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );"""

    cursor.execute(create_table_statement)

    with open('../../second_jaco.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # print(row)

            for key, value in row.items():
                if value == '' or value == '-' and 'street' not in key.lower():
                    row[key] = None
                # print(key, value)

            data = (row['\ufeffHouse/Unit/Lot No.'], row['Floor No.'], row['Building Name'], row['Street Type'] + " " + row['Street Name'], row['Section'], row['City'], row['State'], row['Postcode'],
                    row['unit_num_match (Y/N)'], row['CUSTOMER EMAIL ADDRESS'], row['CUSTOMER CONTACT NUMBER'])

            insert_statement = """
            INSERT INTO cvg_db ( unit_no, floor, building, street, section, city, state, postcode, search_level_flag, notify_email, notify_mobile )
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
            """

            cursor.execute(insert_statement, data)

            cnx.commit()


if __name__ == '__main__':
    upload_to_db()
