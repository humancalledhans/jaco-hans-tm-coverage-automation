import mysql.connector
from src.tm_partners.db_read_write.db_secrets import get_db_password
# from db_secrets import get_db_password
from src.tm_partners.singleton.all_the_data import AllTheData
from src.tm_partners.db_read_write.data_object import DataObject

# from db_secrets import get_db_password
# from current_db_row import CurrentDBRow
# from all_the_data import AllTheData
# from data_object import DataObject


def read_from_db():
    password = get_db_password()
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=password,
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    # query = f"SELECT * FROM cvg_db WHERE is_active = 1 ORDER BY created_at DESC"
    query = f"SELECT * FROM cvg_db ORDER BY created_at DESC"
    # query = "SELECT * FROM cvg_db WHERE id = 140"
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

        all_the_data.add_into_data_list(data_object)

    # id=current_row[0]
    # unit_no=current_row[1]
    # floor=current_row[2]
    # building=current_row[3]
    # street=current_row[4]
    # section=current_row[5]
    # city=current_row[6]
    # state=current_row[7]
    # postcode=current_row[8]
    # search_level_flag=current_row[9]
    # source=current_row[10]
    # source_id=current_row[11]
    # salesman=current_row[12]
    # notify_email=current_row[13]
    # notify_mobile=current_row[14]
    # result_type=current_row[15]
    # result_remark=current_row[16]
    # is_active=current_row[17]
    # created_at=current_row[18]
    # updated_at=current_row[19]

    # data_object=DataObject(id=id, unit_no=unit_no, floor=floor,
    #                          building=building, street=street, section=section,
    #                          city=city, state=state, postcode=postcode,
    #                          search_level_flag=search_level_flag, source=source,
    #                          source_id=source_id, salesman=salesman,
    #                          notify_email=notify_email, notify_mobile=notify_mobile,
    #                          result_type=result_type, result_remark=result_remark,
    #                          is_active=is_active, created_at=created_at,
    #                          updated_at=updated_at)


# if __name__ == '__main__':
    # print(read_from_db(1))
