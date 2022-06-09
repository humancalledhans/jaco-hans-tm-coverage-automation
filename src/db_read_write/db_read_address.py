import mysql.connector
import pandas as pd


def upload_to_db():
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password="ExtInfo!@#",
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

if __name__ == '__main__':
    upload_to_db()
