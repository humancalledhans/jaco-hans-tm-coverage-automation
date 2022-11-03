import mysql.connector

from src.tm_partners.db_read_write.db_secrets import get_db_password
# from db_secrets import get_db_password


def get_column_names():
    password = get_db_password()
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=password,
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    query = f"SHOW columns FROM cvg_db"
    cursor.execute(query)
    result = cursor.fetchall()

    # example return data:
    # [('id', 'int(11)', 'NO', 'PRI', None, 'auto_increment'),
    # ('unit_no', 'varchar(255)', 'YES', '', None, ''),
    # ('floor', 'varchar(255)', 'YES', '', None, ''),
    # ('building', 'varchar(255)', 'YES', '', None, ''),
    # ('street', 'varchar(255)', 'YES', '', None, ''),
    # ('section', 'varchar(255)', 'YES', '', None, ''),
    # ('city', 'varchar(255)', 'YES', '', None, ''),
    # ('state', 'varchar(255)', 'YES', '', None, ''),
    # ('postcode', 'varchar(255)', 'YES', '', None, ''),
    # ('search_level_flag', 'tinyint(4)', 'YES', '', '1', ''),
    # ('source', 'varchar(100)', 'YES', '', None, ''),
    # ('source_id', 'varchar(100)', 'YES', '', None, ''),
    # ('salesman', 'int(11)', 'YES', '', None, ''),
    # ('notify_email', 'varchar(255)', 'YES', '', None, ''),
    # ('notify_mobile', 'varchar(255)', 'YES', '', None, ''),
    # ('result_type', 'int(11)', 'YES', '', None, ''),
    # ('result_remark', 'varchar(255)', 'YES', '', None, ''),
    # ('created_at', 'timestamp', 'NO', '', 'CURRENT_TIMESTAMP', ''),
    # ('updated_at', 'timestamp', 'NO', '', 'CURRENT_TIMESTAMP', 'on update CURRENT_TIMESTAMP')]

    column_names_list = []
    for column in result:
        column_names_list.append(column[0])

    return column_names_list

# if __name__ == '__main__':
    # print(get_column_names())
