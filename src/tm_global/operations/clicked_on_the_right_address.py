import time
from src.tm_global.operations.search_the_exact_address import search_the_exact_address


def clicked_on_the_right_address(driver, a, address):
    """
    address would be in the form of:
    ((['61', 'JALAN', 'TANJUNG 2', 'BUKIT BERUNTUNG', '', '', 'SERENDAH', '48300', 'FTTH', 'Residential'],1), ('BEST MATCH', True))
    """
    address_marks = address[1][0]
    lotNumAndStreetAndPostcodeNumMatchBool = address[1][1]
    address_string = ''
    for str_idx in range(len(address[0][0])-2):
        if address[0][0][str_idx] != '' and address[0][0][str_idx] != ' ' and address[0][0][str_idx].strip() != '-':
            address_string += address[0][str_idx] + ' '

    address_string = address_string.strip()
    print("resultant address string", address_string)

    # search the exact address.
    (driver, a) = search_the_exact_address(driver, a, address_string)

    return (driver, a)
