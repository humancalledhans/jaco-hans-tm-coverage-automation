from abc import ABCMeta, abstractstaticmethod
import threading


class ISelectedTableRow(metaclass=ABCMeta):
    @abstractstaticmethod
    def set_lotnumfound():
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
        self.unit_no = None
        self.street_type = None
        self.street_name = None
        self.section = None
        self.floor = None
        self.building = None
        self.city = None
        self.state = None
        self.postcode = None

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
            self.street_type = selected_table_row_street_type

    @staticmethod
    def set_street_name(self, selected_table_row_street_name):
        if (
            selected_table_row_street_name == "None"
            or selected_table_row_street_name is None
            or len(selected_table_row_street_name) == 0
        ):
            self.street_type = ""
        else:
            self.street_type = selected_table_row_street_name

    @staticmethod
    def set_section(self, selected_table_row_section):
        if (
            selected_table_row_section == "None"
            or selected_table_row_section is None
            or len(selected_table_row_section) == 0
        ):
            self.section = ""
        else:
            self.section = selected_table_row_section

    @staticmethod
    def set_floor(self, selected_table_row_floor):
        if (
            selected_table_row_floor == "None"
            or selected_table_row_floor is None
            or len(selected_table_row_floor) == 0
        ):
            self.floor = ""
        else:
            self.floor = selected_table_row_floor

    @staticmethod
    def set_building(self, selected_table_row_building):
        if (
            selected_table_row_building == "None"
            or selected_table_row_building is None
            or len(selected_table_row_building) == 0
        ):
            self.building = ""
        else:
            self.building = selected_table_row_building

    @staticmethod
    def set_city(self, selected_table_row_city):
        if (
            selected_table_row_city == "None"
            or selected_table_row_city is None
            or len(selected_table_row_city) == 0
        ):
            self.city = ""
        else:
            self.city = selected_table_row_city

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
            self.postcode = selected_table_row_postcode

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
            input_street = " " + self.get_street_name(self=self)
        elif (
            self.get_street_type(self=self) is not None
            and self.get_street_name(self=self) is not None
        ):
            input_street = (
                self.get_street_type(self=self) + " " + self.get_street_name(self=self)
            )
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

        return address_string
