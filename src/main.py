from operations.login import login


def main():
    print("Hi! This is a Coverage Automation System. It will:\n1. Read in a Database of Addresses\n2. Check the coverage of the addresses\n3. Send an email with a screenshot depending on the 4 coverage end results.")
    # four scenarios: 1. within servicable areas, 2. service provider not the same with Transfer Request, 3. outside servicable areas, 4. Another progressing order created on the same address has been detected.

    # four address examples:
    # 1. within servicable areas (No. A-1-8, Floor 1, DATARAN EMARALD Building, JALAN PS 11 Section PRIMA SELAYANG, 68100 BATU CAVES SELANGOR, MALAYSIA)
    # 2. service provider not the same with Transfer Request (No. 12, Floor -, JALAN DAGANG JAYA, 68000 AMPAND SELANGOR, MALAYSIA)
    # 3. outside servicable areas (No. C4-6-2, Floor 6, FTTH EVERGREEN PARK CYPRESS CONDOMINIUM BLOK C4 BUilding. PERSIARAN SUNGAI LONG 1 Section BANDAR SUNGAI LONG, 43000 KALANG SELANGOR, MALAYSIA)
    # 4. Another progressing order created on the same address has been detected (No. 38, JALAN SS 26/7 Section TAMAN MAYANG JAYA, 47301 PETALING JAYA SELANGOR, MALAYSIA)
    # path_to_csv = input(
    #     "Please ensure you have a 'partners_coveragecheck.csv' file in the same directory. Press 'Enter' Key to confirm.")
    # login('DPSL9701', 'Djns513!!')
    login('DPPJ1901', 'Dsync110!!')
    # print("Would you like the coverage test to match the ones given in the table?")
    # print("1. Only for the addresses without Building Name.") # will not work. because the addresses with building names might require further uni no specified as well.
    # print("2. Yes - match for all the addresses.")
    # print("3. No - do not match for all the addresses.")

    # analysis on the xpath for the table results:
    # when there's only one result (without the filter boxes), the xpath for the tr @class is "[@class='datagrid-even']"
    # when there's multiple results (with the filter boxes), the xpath for the tr @class is "[@class='odd' or @class='even']"
    # after you filter using the filter box, the xpath would be //tr[@class='odd' or @class='even'][not(@style)]


if __name__ == '__main__':
    main()
