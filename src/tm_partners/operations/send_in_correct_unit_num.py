from src.tm_partners.singleton.current_db_row import CurrentDBRow
import re


def preprocess_unit_num():
    current_db_row = CurrentDBRow.get_instance()
    hse_unit_lotno_to_send = ''
    hse_unit_lotno = current_db_row.get_house_unit_lotno(
        self=current_db_row).strip()
    integer_regex = re.compile('^[0-9]+$')
    if ',' in hse_unit_lotno:
        strng_lst = hse_unit_lotno.split(',')
        for strng in strng_lst:
            if 'LOT' in strng.upper() or 'UNIT' in strng.upper() or 'NO' in strng.upper() or 'BLOCK' in strng.upper() or 'BLOK' in strng.upper() or integer_regex.search(strng):
                hse_unit_lotno_to_send = strng
                break
        if hse_unit_lotno_to_send == '':
            hse_unit_lotno_to_send = strng_lst[0].strip()
    else:
        if hse_unit_lotno_to_send == '':
            hse_unit_lotno_to_send = hse_unit_lotno

    return hse_unit_lotno_to_send.strip()
