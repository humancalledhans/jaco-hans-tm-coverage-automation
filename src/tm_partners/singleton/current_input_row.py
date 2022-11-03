from abc import ABCMeta, abstractstaticmethod
import re


class ICurrentInputRow(metaclass=ABCMeta):

    @abstractstaticmethod
    def set_accepted_states_list():
        """ to implement in child class """

    @abstractstaticmethod
    def set_accepted_street_types_list():
        """ to implement in child class """

    @abstractstaticmethod
    def set_id():
        """ to implement in child class """

    @abstractstaticmethod
    def set_unit_no():
        """ to implement in child class """

    @abstractstaticmethod
    def set_floor():
        """ to implement in child class """

    @abstractstaticmethod
    def set_building():
        """ to implement in child class """

    @abstractstaticmethod
    def set_street():
        """ to implement in child class """

    @abstractstaticmethod
    def set_section():
        """ to implement in child class """

    @abstractstaticmethod
    def set_city():
        """ to implement in child class """

    @abstractstaticmethod
    def set_state():
        """ to implement in child class """

    @abstractstaticmethod
    def set_postcode():
        """ to implement in child class """

    @abstractstaticmethod
    def set_search_level_flag():
        """ to implement in child class """

    @abstractstaticmethod
    def set_source():
        """ to implement in child class """

    @abstractstaticmethod
    def set_source_id():
        """ to implement in child class """

    @abstractstaticmethod
    def set_salesman():
        """ to implement in child class """

    @abstractstaticmethod
    def set_notify_email():
        """ to implement in child class """

    @abstractstaticmethod
    def set_notify_mobile():
        """ to implement in child class """

    @abstractstaticmethod
    def set_result_type():
        """ to implement in child class """

    @abstractstaticmethod
    def set_result_remark():
        """to implement in child class """

    @abstractstaticmethod
    def set_is_active():
        """ to implement in child class """

    @abstractstaticmethod
    def set_created_at():
        """ to implement in child class """

    @abstractstaticmethod
    def set_updated_at():
        """ to implement in child class """

    @abstractstaticmethod
    def get_accepted_states_list():
        """ to implement in child class """

    @abstractstaticmethod
    def get_accepted_street_types_list():
        """ to implement in child class """

    @abstractstaticmethod
    def get_input_header_data():
        """ to implement in child class """

    @abstractstaticmethod
    def get_input_row_data():
        """ to implement in child class """

    @abstractstaticmethod
    def get_id():
        """ to implement in child class """

    @abstractstaticmethod
    def get_house_unit_lotno():
        """ to implement in child class """

    @abstractstaticmethod
    def get_floor():
        """ to implement in child class """

    @abstractstaticmethod
    def get_building():
        """ to implement in child class """

    @abstractstaticmethod
    def get_street():
        """ to implement in child class """

    @abstractstaticmethod
    def get_section():
        """ to implement in child class """

    @abstractstaticmethod
    def get_city():
        """ to implement in child class """

    @abstractstaticmethod
    def get_state():
        """ to implement in child class """

    @abstractstaticmethod
    def get_postcode():
        """ to implement in child class """

    @abstractstaticmethod
    def get_search_level_flag():
        """ to implement in child class """

    @abstractstaticmethod
    def get_source():
        """ to implement in child class """

    @abstractstaticmethod
    def get_source_id():
        """ to implement in child class """

    @abstractstaticmethod
    def get_salesman():
        """ to implement in child class """

    @abstractstaticmethod
    def get_notify_email():
        """ to implement in child class """

    @abstractstaticmethod
    def get_notify_mobile():
        """ to implement in child class """

    @abstractstaticmethod
    def get_is_active():
        """ to implement in child class """

    @abstractstaticmethod
    def get_result_type():
        """ to implement in child class """

    @abstractstaticmethod
    def get_created_at():
        """ to implement in child class """

    @abstractstaticmethod
    def get_updated_at():
        """ to implement in child class """


class CurrentInputRow(ICurrentInputRow):

    __instance = None

    @staticmethod
    def get_instance():
        if CurrentInputRow.__instance is None:
            CurrentInputRow(
                accepted_states_list=None, accepted_street_types_list=None)
        return CurrentInputRow.__instance

    def __init__(self, accepted_states_list=None, accepted_street_types_list=None):
        if CurrentInputRow.__instance is not None:
            raise Exception(
                "CurrentInputRow instance cannot be instantiated more than once!")
        else:
            CurrentInputRow.__instance = self
            self.accepted_states_list = accepted_states_list
            self.accepted_street_types_list = accepted_street_types_list
            self.current_row_id = None
            self.current_row_unit_no = None
            self.current_row_floor = None
            self.current_row_building = None
            self.current_row_street = None
            self.current_row_section = None
            self.current_row_city = None
            self.current_row_state = None
            self.current_row_postcode = None
            self.current_row_search_level_flag = None
            self.current_row_source = None
            self.current_row_source_id = None
            self.current_row_salesman = None
            self.current_row_notify_email = None
            self.current_row_notify_mobile = None
            self.current_row_result_type = None
            self.current_row_result_remark = None
            self.current_row_is_active = None
            self.current_row_created_at = None
            self.current_row_updated_at = None

    @staticmethod
    def set_accepted_states_list(self, accepted_states_list):
        self.accepted_states_list = accepted_states_list

    @staticmethod
    def set_accepted_street_types_list(self, accepted_street_types_list):
        self.accepted_street_types_list = accepted_street_types_list

    @staticmethod
    def set_id(self, current_row_id):
        self.current_row_id = current_row_id

    @staticmethod
    def set_unit_no(self, current_row_unit_no):
        if current_row_unit_no == 'None' or current_row_unit_no is None or len(current_row_unit_no) == 0:
            self.current_row_unit_no = ''
        else:
            int_as_string_lst = ['0', '1', '2',
                                 '3', '4', '5', '6', '7', '8', '9']
            if '-' in current_row_unit_no and current_row_unit_no[-1] in int_as_string_lst:
                x = re.split("-", current_row_unit_no)

                for idx in range(len(x)-1, 0, -1):
                    if x[idx] not in int_as_string_lst:
                        continue
                    else:
                        x[idx] = "0" + x[idx]

            self.current_row_unit_no = current_row_unit_no

    @staticmethod
    def set_floor(self, current_row_floor):
        if current_row_floor == 'None' or current_row_floor is None or len(current_row_floor) == 0:
            self.current_row_floor = ''
        else:
            self.current_row_floor = current_row_floor

    @staticmethod
    def set_building(self, current_row_building):
        if current_row_building == 'None' or current_row_building is None or len(current_row_building) == 0:
            self.current_row_building = ''
        else:
            self.current_row_building = current_row_building

    @staticmethod
    def set_street(self, current_row_street):
        if current_row_street == 'None' or current_row_street is None or len(current_row_street) == 0:
            self.current_row_street = ''
        else:
            self.current_row_street = current_row_street

    @staticmethod
    def set_section(self, current_row_section):
        if current_row_section == 'None' or current_row_section is None or len(current_row_section) == 0:
            self.current_row_section = ''
        else:
            self.current_row_section = current_row_section

    @staticmethod
    def set_city(self, current_row_city):
        if current_row_city == 'None' or current_row_city is None or len(current_row_city) == 0:
            self.current_row_city = ''
        else:
            self.current_row_city = current_row_city

    @staticmethod
    def set_state(self, current_row_state):
        if current_row_state == 'None' or current_row_state is None or len(current_row_state) == 0:
            self.current_row_state = ''
        else:
            self.current_row_state = current_row_state

    @staticmethod
    def set_postcode(self, current_row_postcode):
        if current_row_postcode == 'None' or current_row_postcode is None or len(current_row_postcode) == 0:
            self.current_row_postcode = ''
        else:
            self.current_row_postcode = current_row_postcode

    @staticmethod
    def set_search_level_flag(self, current_row_search_level_flag):
        if current_row_search_level_flag == 'None' or current_row_search_level_flag is None or current_row_search_level_flag != 1:
            self.current_row_search_level_flag = 0
        else:
            self.current_row_search_level_flag = current_row_search_level_flag

    @staticmethod
    def set_source(self, current_row_source):
        self.current_row_source = current_row_source

    @staticmethod
    def set_source_id(self, current_row_source_id):
        self.current_row_source_id = current_row_source_id

    @staticmethod
    def set_salesman(self, current_row_salesman):
        self.current_row_salesman = current_row_salesman

    @staticmethod
    def set_notify_email(self, current_row_notify_email):
        self.current_row_notify_email = current_row_notify_email

    @staticmethod
    def set_notify_mobile(self, current_row_notify_mobile):
        self.current_row_notify_mobile = current_row_notify_mobile

    @staticmethod
    def set_result_type(self, current_row_result_type):
        self.current_row_result_type = current_row_result_type

    @staticmethod
    def set_result_remark(self, current_row_result_remark):
        self.current_row_result_remark = current_row_result_remark

    @staticmethod
    def set_is_active(self, current_row_is_active):
        self.is_active = current_row_is_active

    @staticmethod
    def set_created_at(self, current_row_created_at):
        self.current_row_created_at = current_row_created_at

    @staticmethod
    def set_updated_at(self, current_row_updated_at):
        self.current_row_updated_at = current_row_updated_at

    @staticmethod
    def get_accepted_states_list(self):
        return self.accepted_states_list

    @staticmethod
    def get_accepted_street_types_list(self):
        return self.accepted_street_types_list

    @staticmethod
    def get_input_header_data(self):
        return self.input_header_data

    @staticmethod
    def get_input_row_data(self):
        return self.input_row_data

    @staticmethod
    def get_id(self):
        return self.current_row_id

    @staticmethod
    def get_house_unit_lotno(self):
        return self.current_row_unit_no

    @staticmethod
    def get_floor(self):
        return self.current_row_floor

    @staticmethod
    def get_building(self):
        return self.current_row_building

    @staticmethod
    def get_street(self):
        return self.current_row_street

    @staticmethod
    def get_section(self):
        return self.current_row_section

    @staticmethod
    def get_city(self):
        return self.current_row_city

    @staticmethod
    def get_state(self):
        return self.current_row_state

    @staticmethod
    def get_postcode(self):
        return self.current_row_postcode

    @staticmethod
    def get_search_level_flag(self):
        return self.current_row_search_level_flag

    @staticmethod
    def get_source(self):
        return self.current_row_source

    @staticmethod
    def get_source_id(self):
        return self.current_row_source_id

    @staticmethod
    def get_salesman(self):
        return self.current_row_salesman

    @staticmethod
    def get_notify_email(self):
        return self.current_row_notify_email

    @staticmethod
    def get_notify_mobile(self):
        return self.current_row_notify_mobile

    @staticmethod
    def get_result_type(self):
        return self.current_row_result_type

    @staticmethod
    def get_result_remark(self):
        return self.current_row_result_remark

    @staticmethod
    def get_is_active(self):
        return self.is_active

    @staticmethod
    def get_created_at(self):
        return self.current_row_created_at

    @staticmethod
    def get_updated_at(self):
        return self.current_row_updated_at

    @staticmethod
    def get_address(self):
        input_house_unit_lotno = self.get_house_unit_lotno(
            self=self)
        input_street = self.get_street(self=self)
        input_section = self.get_section(self=self)
        input_floor_no = self.get_floor(self=self)
        input_building_name = self.get_building(
            self=self)
        input_city = self.get_city(self=self)
        input_state = self.get_state(self=self)
        input_postcode = self.get_postcode(self=self)

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

        address_string = "House/Unit/Lot No. " + input_house_unit_lotno + '\n' + \
"Street: " + input_street + '\n' + \
"Section: " + input_section + '\n' + \
"Floor No: " + input_floor_no + '\n' + \
"Building Name: " + input_building_name + '\n' + \
"City: " + input_city + '\n' + \
"State: " + input_state + '\n' + \
"Postcode: " + input_postcode

        return address_string
