from abc import ABCMeta, abstractstaticmethod
import time
import threading


class ISelectedTableRow(metaclass=ABCMeta):
    @abstractstaticmethod
    def set_lotnumfound():
        """to implement in child class"""

    @abstractstaticmethod
    def set_is_best_match():
        """to implement in child class"""

    @abstractstaticmethod
    def set_unit_no():
        """to implement in child class"""

    @abstractstaticmethod
    def set_street_type():
        """to implement in child class"""

    @abstractstaticmethod
    def set_street_name():
        """to implement in child class"""

    @abstractstaticmethod
    def set_section():
        """to implement in child class"""

    @abstractstaticmethod
    def set_floor():
        """to implement in child class"""

    @abstractstaticmethod
    def set_building():
        """to implement in child class"""

    @abstractstaticmethod
    def set_city():
        """to implement in child class"""

    @abstractstaticmethod
    def set_state():
        """to implement in child class"""

    @abstractstaticmethod
    def set_postcode():
        """to implement in child class"""

    @abstractstaticmethod
    def set_result_type():
        """to implement in child class"""

    @abstractstaticmethod
    def set_result_remark():
        """to implement in child class"""

    @abstractstaticmethod
    def set_part_of_address_used():
        """to implement in child class"""

    @abstractstaticmethod
    def set_used_lot_num_as_filter():
        """to implement in child class"""

    @abstractstaticmethod
    def set_used_building_name_as_filter():
        """to implement in child class"""

    @abstractstaticmethod
    def set_used_street_name_as_filter():
        """to implement in child class"""

    @abstractstaticmethod
    def set_used_section_name_as_filter():
        """to implement in child class"""

    @abstractstaticmethod
    def get_is_best_match():
        """to implement in child class"""

    @abstractstaticmethod
    def get_unit_no():
        """to implement in child class"""

    @abstractstaticmethod
    def get_street_type():
        """to implement in child class"""

    @abstractstaticmethod
    def get_street_name():
        """to implement in child class"""

    @abstractstaticmethod
    def get_section():
        """to implement in child class"""

    @abstractstaticmethod
    def get_floor():
        """to implement in child class"""

    @abstractstaticmethod
    def get_building():
        """to implement in child class"""

    @abstractstaticmethod
    def get_city():
        """to implement in child class"""

    @abstractstaticmethod
    def get_state():
        """to implement in child class"""

    @abstractstaticmethod
    def get_postcode():
        """to implement in child class"""

    @abstractstaticmethod
    def get_address():
        """to implement in child class"""

    @abstractstaticmethod
    def get_result_remark():
        """to implement in child class"""

    @abstractstaticmethod
    def get_part_of_address_used():
        """to implement in child class"""

    @abstractstaticmethod
    def get_used_building_name_as_filter():
        """to implement in child class"""

    @abstractstaticmethod
    def get_used_street_name_as_filter():
        """to implement in child class"""

    @abstractstaticmethod
    def get_used_section_name_as_filter():
        """to implement in child class"""

    @abstractstaticmethod
    def get_used_lot_num_as_filter():
        """to implement in child class"""

    @abstractstaticmethod
    def get_filters_used_to_search():
        """to implement in child class"""


class SelectedTableRow(ISelectedTableRow):
    @staticmethod
    def get_instance():
        local = threading.current_thread().__dict__
        try:
            instance = local["selected_table_row_instance"]
        except KeyError:
            local["selected_table_row_instance"] = SelectedTableRow()
            instance = local["selected_table_row_instance"]
        if instance is None:
            instance = SelectedTableRow()
        return instance

    def __init__(self):
        self.lotnumfound = None
        self.isbestmatch = False
        self.unit_no = None
        self.street_type = None
        self.street_name = None
        self.section = None
        self.floor = None
        self.building = None
        self.city = None
        self.state = None
        self.postcode = None
        self.result_type = None
        self.result_remark = None
        self.part_of_address_used = None
        self.used_building_name_as_filter = None
        self.used_street_name_as_filter = None
        self.used_section_name_as_filter = None
        self.used_lot_num_as_filter = None
        self.used_city_name_as_filter = None
        self.used_postcode_as_filter = None

    @staticmethod
    def set_lotnumfound(self, lotnumfound):
        self.lotnumfound = lotnumfound

    @staticmethod
    def set_unit_no(self, selected_table_row_unit_no):
        # if selected_table_row_unit_no == 'None' or selected_table_row_unit_no is None or len(selected_table_row_unit_no) == 0:
        #     self.selected_table_row_unit_no = ''
        # elif selected_table_row_unit_no == 'PENTHOUSE':
        #     self.unit_no = 'PENTHOUSE'
        # else:
        #     int_as_string_lst = ['0', '1', '2',
        #                          '3', '4', '5', '6', '7', '8', '9']
        #     if '-' in selected_table_row_unit_no and selected_table_row_unit_no[-1] in int_as_string_lst:
        #         x = re.split("-", selected_table_row_unit_no)

        #         for idx in range(len(x)-1, 0, -1):
        #             if x[idx] not in int_as_string_lst:
        #                 continue
        #             else:
        #                 x[idx] = "0" + x[idx]

        self.unit_no = selected_table_row_unit_no

    @staticmethod
    def set_street_type(self, selected_table_row_street_type):
        if (
            selected_table_row_street_type == "None"
            or selected_table_row_street_type is None
            or len(selected_table_row_street_type) == 0
        ):
            self.street_type = ""
        else:
            self.street_type = selected_table_row_street_type.strip()

    @staticmethod
    def set_street_name(self, selected_table_row_street_name):
        if (
            selected_table_row_street_name == "None"
            or selected_table_row_street_name is None
            or len(selected_table_row_street_name) == 0
        ):
            self.street_name = ""
        else:
            self.street_name = selected_table_row_street_name.strip()

    @staticmethod
    def set_section(self, selected_table_row_section):
        if (
            selected_table_row_section == "None"
            or selected_table_row_section is None
            or len(selected_table_row_section) == 0
        ):
            self.section = ""
        else:
            self.section = selected_table_row_section.strip()

    @staticmethod
    def set_floor(self, selected_table_row_floor):
        if (
            selected_table_row_floor == "None"
            or selected_table_row_floor is None
            or len(selected_table_row_floor) == 0
        ):
            self.floor = ""
        else:
            self.floor = selected_table_row_floor.strip()

    @staticmethod
    def set_building(self, selected_table_row_building):
        if (
            selected_table_row_building == "None"
            or selected_table_row_building is None
            or len(selected_table_row_building) == 0
        ):
            self.building = ""
        else:
            self.building = selected_table_row_building.strip()

    @staticmethod
    def set_city(self, selected_table_row_city):
        if (
            selected_table_row_city == "None"
            or selected_table_row_city is None
            or len(selected_table_row_city) == 0
        ):
            self.city = ""
        else:
            self.city = selected_table_row_city.strip()

    @staticmethod
    def set_state(self, selected_table_row_state):
        if (
            selected_table_row_state == "None"
            or selected_table_row_state is None
            or len(selected_table_row_state) == 0
        ):
            self.state = ""
        else:
            self.state = selected_table_row_state

    @staticmethod
    def set_postcode(self, selected_table_row_postcode):
        if (
            selected_table_row_postcode == "None"
            or selected_table_row_postcode is None
            or len(selected_table_row_postcode) == 0
        ):
            self.postcode = ""
        else:
            self.postcode = selected_table_row_postcode.strip()

    @staticmethod
    def set_result_remark(self, result_remark):

        # all result remarks:
        # 'THE ADDRESS FOUND IS WITHIN THE SERVICEABLE AREA'
        # 'No matching lot number results, and Lot Number match bool = 1.'
        # 'THE ADDRESS FOUND IS NOT SERVICEABLE DUE TO: PORT FULL'
        # 'THE ADDRESS FOUND IS WITHIN THE SERVICEABLE AREA BUT REQUIRE NEW INFRA DEVELOPMENT. PLEASE BE INFORMED ANY CANCELLATION RELATED TO NEW INFRA IS SUBJECT TO CANCELLATION FEES.'

        if result_remark == "THE ADDRESS FOUND IS WITHIN THE SERVICEABLE AREA":
            self.result_remark = "Within Serviceable Area."
        elif (
            result_remark
            == "No matching lot number results, and Lot Number match bool = 1."
        ):  # no lot number found
            self.result_remark = "No Lot Number Found, but Lot Num Match = 1"
        elif result_remark == "THE ADDRESS FOUND IS NOT SERVICEABLE DUE TO: PORT FULL":
            self.result_remark = "Not Serviceable - Port Full"
        elif (
            result_remark
            == "THE ADDRESS FOUND IS WITHIN THE SERVICEABLE AREA BUT REQUIRE NEW INFRA DEVELOPMENT. PLEASE BE INFORMED ANY CANCELLATION RELATED TO NEW INFRA IS SUBJECT TO CANCELLATION FEES."
        ):
            self.result_remark = "Within Servicable Area, Require New Infra Development"
        elif result_remark == "No results found.":
            self.result_remark = "No results found."
        elif (
            result_remark
            == "Sorry, the address in our database is incomplete based on your inputs. Please try searching again."
        ):
            self.result_remark = "Incomplete Address."
        elif (
            result_remark
            == "Street Name Found, Lot Number Not Found, and Lot Number match bool = 1."
        ):
            self.result_remark = "Street Name Found, Lot Number Not Found, and Lot Number match bool = 1."
        else:
            time.sleep(5)
            print("NEW RESULT REMARK", result_remark)
            # if result_remark == 'No matching lot number results, and Lot Number match bool = 1.'
        #     self.set_result_type(
        #         self=self, result_type=3)

    @staticmethod
    def set_result_type(self, result_type):
        self.result_type = result_type.strip()

    @staticmethod
    def set_is_best_match(self, is_best_match):
        self.is_best_match = is_best_match

    @staticmethod
    def set_part_of_address_used(self, part_of_address_used):
        self.part_of_address_used = part_of_address_used.strip()

    @staticmethod
    def set_used_lot_num_as_filter(self, used_lot_num_as_filter):
        self.used_lot_num_as_filter = used_lot_num_as_filter

    @staticmethod
    def set_used_building_name_as_filter(self, used_building_name_as_filter):
        self.used_building_name_as_filter = used_building_name_as_filter

    @staticmethod
    def set_used_street_name_as_filter(self, used_street_name_as_filter):
        self.used_street_name_as_filter = used_street_name_as_filter

    @staticmethod
    def set_used_section_name_as_filter(self, used_section_name_as_filter):
        self.used_section_name_as_filter = used_section_name_as_filter

    @staticmethod
    def set_used_city_name_as_filter(self, used_city_name_as_filter):
        self.used_city_name_as_filter = used_city_name_as_filter

    @staticmethod
    def set_used_postcode_as_filter(self, used_postcode_as_filter):
        self.used_postcode_as_filter = used_postcode_as_filter

    @staticmethod
    def get_is_best_match(self):
        return self.is_best_match

    @staticmethod
    def get_unit_no(self):
        return self.unit_no

    @staticmethod
    def get_street_type(self):
        return self.street_type

    @staticmethod
    def get_street_name(self):
        return self.street_name

    @staticmethod
    def get_section(self):
        return self.section

    @staticmethod
    def get_floor(self):
        return self.floor

    @staticmethod
    def get_building(self):
        return self.building

    @staticmethod
    def get_city(self):
        return self.city

    @staticmethod
    def get_state(self):
        return self.state

    @staticmethod
    def get_postcode(self):
        return self.postcode

    @staticmethod
    def get_address(self):
        input_house_unit_lotno = self.get_unit_no(self=self)
        if (
            self.get_street_type(self=self) is None
            and self.get_street_name(self=self) is not None
        ):
            input_street = self.get_street_name(self=self)
        elif (
            self.get_street_type(self=self) is not None
            and self.get_street_name(self=self) is not None
        ):
            input_street = (
                self.get_street_type(self=self) + " " + self.get_street_name(self=self)
            )
        elif (
            self.get_street_type(self=self) is not None
            and self.get_street_name(self=self) is None
        ):
            input_street = self.get_street_type(self=self)
        else:
            input_street = ""
        input_section = self.get_section(self=self)
        input_floor_no = self.get_floor(self=self)
        input_building_name = self.get_building(self=self)
        input_city = self.get_city(self=self)
        input_state = self.get_state(self=self)
        input_postcode = self.get_postcode(self=self)

        if input_house_unit_lotno is None:
            input_house_unit_lotno = ""
        if input_street is None:
            input_street = ""
        if input_section is None:
            input_section = ""
        if input_floor_no is None:
            input_floor_no = ""
        if input_building_name is None:
            input_building_name = ""
        if input_city is None:
            input_city = ""
        if input_state is None:
            input_state = ""
        if input_postcode is None:
            input_postcode = ""

        address_string = (
            input_house_unit_lotno
            + " "
            + input_street
            + " "
            + input_section
            + " "
            + input_floor_no
            + " "
            + input_building_name
            + " "
            + input_city
            + input_state
            + " "
            + input_postcode
        )

        # address_string = "House/Unit/Lot No: " + input_house_unit_lotno + '\n' + \
        #     "Street: " + input_street + '\n' + \
        #     "Section: " + input_section + '\n' + \
        #     "Floor No: " + input_floor_no + '\n' + \
        #     "Building Name: " + input_building_name + '\n' + \
        #     "City: " + input_city + '\n' + \
        #     "State: " + input_state + '\n' + \
        #     "Postcode: " + input_postcode

        return address_string.strip()

    @staticmethod
    def get_result_remark(self):
        return self.result_remark

    @staticmethod
    def get_part_of_address_used(self):
        return self.part_of_address_used

    @staticmethod
    def get_used_building_name_as_filter(self):
        return self.used_building_name_as_filter

    @staticmethod
    def get_used_street_name_as_filter(self):
        return self.used_street_name_as_filter

    @staticmethod
    def get_used_section_name_as_filter(self):
        return self.used_section_name_as_filter

    @staticmethod
    def get_used_lot_num_as_filter(self):
        return self.used_lot_num_as_filter

    @staticmethod
    def get_used_city_name_as_filter(self):
        return self.used_city_name_as_filter

    @staticmethod
    def get_used_postcode_as_filter(self):
        return self.used_postcode_as_filter

    @staticmethod
    def get_filters_used_to_search(self):
        res = []
        if self.get_used_city_name_as_filter(self=self):
            res.append("City Name")
        if self.get_used_postcode_as_filter(self=self):
            res.append("Postcode")
        if self.get_used_section_name_as_filter(self=self):
            res.append("Section Name")
        if self.get_used_street_name_as_filter(self=self):
            res.append("Street Name")
        if self.get_used_building_name_as_filter(self=self):
            res.append("Building Name")
        if self.get_used_lot_num_as_filter(self=self):
            res.append("Lot Number")
        return res

    @staticmethod
    def reset_all_values(self):
        self.lotnumfound = None
        self.isbestmatch = False
        self.unit_no = None
        self.street_type = None
        self.street_name = None
        self.section = None
        self.floor = None
        self.building = None
        self.city = None
        self.state = None
        self.postcode = None
        self.result_type = None
        self.result_remark = None
        self.part_of_address_used = None
        self.used_building_name_as_filter = None
        self.used_street_name_as_filter = None
        self.used_section_name_as_filter = None
        self.used_lot_num_as_filter = None
