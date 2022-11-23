import requests
from src.tm_global.db_read_write.db_get_chat_id import get_chat_id
from src.tm_global.singleton.current_db_row import CurrentDBRow


def send_message(msg):
    current_db_row = CurrentDBRow.get_instance()
    phone_num_list = current_db_row.get_notify_mobile(
        self=current_db_row).split(',')

    # to take away same phone numbers in a list.
    phone_num_list = list(set(phone_num_list))

    try:
        helper_send_message(msg, phone_num_list=phone_num_list)
    except Exception as e:
        print(e)


def helper_send_message(msg, phone_num_list):

    TOKEN = "5558294620:AAGKJDU0ja0ys_0T2-4JhVGx-3XJ1zJRtow"
    # text = "JacoHansCABot speaks"
    address_string = ''
    current_db_row = CurrentDBRow.get_instance()
    input_house_unit_lotno = current_db_row.get_house_unit_lotno(
        self=current_db_row)
    input_street = current_db_row.get_street(
        self=current_db_row)
    input_section = current_db_row.get_section(
        self=current_db_row)
    input_floor_no = current_db_row.get_floor(
        self=current_db_row)
    input_building_name = current_db_row.get_building(
        self=current_db_row)
    input_city = current_db_row.get_city(self=current_db_row)
    input_state = current_db_row.get_state(
        self=current_db_row)
    input_postcode = current_db_row.get_postcode(
        self=current_db_row)

    if input_house_unit_lotno is None:
        input_house_unit_lotno = ''
    if input_street is None:
        input_street = ''
    if input_section is None:
        input_section = ''
    if input_floor_no is None:
        input_floor_no = ''
    if input_building_name is None:
        input_building_name = ''
    if input_city is None:
        input_city = ''
    if input_state is None:
        input_state = ''
    if input_postcode is None:
        input_postcode = ''

    address_string = address_string + \
        "House/Unit/Lot No." + input_house_unit_lotno + '\n' + \
        "Street: " + input_street + '\n' + \
        "Section: " + input_section + '\n' + \
        "Floor No: " + input_floor_no + '\n' + \
        "Building Name: " + input_building_name + '\n' + \
        "City: " + input_city + '\n' + \
        "State: " + input_state + '\n' + \
        "Postcode: " + input_postcode

    for elem in phone_num_list:
        # for every phone number.
        try:
            chat_id = get_chat_id(elem.strip())
            print("CHAT ID", chat_id)

            text = address_string + msg
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
            # url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            r = requests.get(url)

        except IndexError:
            current_row_id = current_db_row.get_id(self=current_db_row)
            raise Exception(f"No chat id found for row id {current_row_id}")


if __name__ == '__main__':
    print(send_message('asdfasdfasdfasf'))
