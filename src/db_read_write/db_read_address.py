import mysql.connector
from src.db_read_write.db_secrets import get_db_password
# from db_secrets import get_db_password
from src.singleton.current_input_row import CurrentInputRow


def read_from_db(id):
    password = get_db_password()
    cnx = mysql.connector.connect(user="oursspc1_db_extuser", password=password,
                                  host="103.6.198.226", port='3306', database="oursspc1_db_cvg")
    cursor = cnx.cursor()

    query = f"SELECT * FROM cvg_db WHERE id = {id}"
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    cnx.close()

    current_input_row = CurrentInputRow.get_instance()

    current_row = result[0]

    current_input_row.set_id(self=current_input_row,
                             current_row_id=current_row[0])
    current_input_row.set_unit_no(
        self=current_input_row, current_row_unit_no=current_row[1])
    current_input_row.set_floor(
        self=current_input_row, current_row_floor=current_row[2])
    current_input_row.set_building(
        self=current_input_row, current_row_building=current_row[3])
    current_input_row.set_street(
        self=current_input_row, current_row_street=current_row[4])
    current_input_row.set_section(
        self=current_input_row, current_row_section=current_row[5])
    current_input_row.set_city(
        self=current_input_row, current_row_city=current_row[6])
    current_input_row.set_state(
        self=current_input_row, current_row_state=current_row[7])
    current_input_row.set_postcode(
        self=current_input_row, current_row_postcode=current_row[8])
    current_input_row.set_search_level_flag(
        self=current_input_row, current_row_search_level_flag=current_row[9])
    current_input_row.set_source(
        self=current_input_row, current_row_source=current_row[10])
    current_input_row.set_source_id(
        self=current_input_row, current_row_source_id=current_row[11])
    current_input_row.set_salesman(
        self=current_input_row, current_row_salesman=current_row[12])
    current_input_row.set_notify_email(
        self=current_input_row, current_row_notify_email=current_row[13])
    current_input_row.set_notify_mobile(
        self=current_input_row, current_row_notify_mobile=current_row[14])
    current_input_row.set_result_type(
        self=current_input_row, current_row_result_type=current_row[15])
    current_input_row.set_result_remark(
        self=current_input_row, current_row_result_remark=current_row[16])
    current_input_row.set_is_active(
        self=current_input_row, current_row_is_active=current_row[17])
    current_input_row.set_created_at(
        self=current_input_row, current_row_created_at=current_row[18])
    current_input_row.set_updated_at(
        self=current_input_row, current_row_updated_at=current_row[19])


# if __name__ == '__main__':
    # print(read_from_db(1))
