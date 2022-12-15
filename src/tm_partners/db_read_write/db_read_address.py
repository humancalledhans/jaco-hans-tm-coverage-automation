import mysql.connector
from src.tm_partners.db_read_write.db_secrets import get_db_password
# from db_secrets import get_db_password
from src.tm_partners.singleton.all_the_data import AllTheData
from src.tm_partners.db_read_write.data_object import DataObject
from src.tm_partners.singleton.data_id_range import DataIdRange

# from db_secrets import get_db_password
# from current_db_row import CurrentDBRow
# from all_the_data import AllTheData
# from data_object import DataObject


def read_from_db(not_null=''):
    password = get_db_password()
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=password,
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    data_id_range = DataIdRange.get_instance()
    start_id = data_id_range.get_start_id(
        self=data_id_range)
    end_id = data_id_range.get_end_id(self=data_id_range)

    print('start id', start_id)
    print('end id', end_id)

    if start_id == end_id:
        query = f"SELECT * FROM cvg_db WHERE id = {start_id}"
    elif not_null != '':
        # query filter exists
        if not_null in ['BUILDING', 'building']:
            query = f"SELECT * FROM cvg_db WHERE id <= {end_id} and id >= {start_id} and {not_null} IS NOT NULL ORDER BY created_at DESC"
        else:
            not_null = ''
            print('Invalid filter requested.')
    else:
        # query = f"SELECT * FROM cvg_db WHERE is_active = 1 ORDER BY created_at DESC"
        query = f"SELECT * FROM cvg_db WHERE id <= {end_id} and id >= {start_id} ORDER BY created_at DESC"
        # query = f"SELECT * FROM cvg_db ORDER BY created_at ASC"
    cursor.execute(query)
    result = cursor.fetchall()

    # get index of each column name.
    query = 'SHOW COLUMNS FROM oursspc1_db_cvg.cvg_db'
    cursor.execute(query)
    result2 = cursor.fetchall()

    all_the_column_names = []
    for i in result2:
        all_the_column_names.append(i[0])

    # print("RESULT", result)

    cursor.close()
    cnx.close()

    all_the_data = AllTheData.get_instance()
    for elem in result:

        data_object = DataObject(id=elem[all_the_column_names.index('id')], unit_no=elem[all_the_column_names.index('unit_no')], floor=elem[all_the_column_names.index('floor')], building=elem[all_the_column_names.index('building')],
                                 street=elem[all_the_column_names.index('street')], section=elem[all_the_column_names.index(
                                     'section')], city=elem[all_the_column_names.index('city')], state=elem[all_the_column_names.index('state')],
                                 postcode=elem[all_the_column_names.index('postcode')], search_level_flag=elem[all_the_column_names.index(
                                     'search_level_flag')], source=elem[all_the_column_names.index('source')], source_id=all_the_column_names.index('source_id'),
                                 salesman=elem[all_the_column_names.index('salesman')], notify_email=elem[all_the_column_names.index(
                                     'notify_email')], notify_mobile=elem[all_the_column_names.index('notify_mobile')], result_type=elem[all_the_column_names.index('result_type')],
                                 result_remark=elem[all_the_column_names.index('result_remark')], is_active=elem[all_the_column_names.index('is_active')], created_at=elem[all_the_column_names.index('created_at')], updated_at=elem[all_the_column_names.index('updated_at')])

        all_the_data.add_into_data_list(self=all_the_data, data=data_object)
