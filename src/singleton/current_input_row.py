from abc import ABCMeta, abstractstaticmethod


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
            self.accepted_states_list = accepted_states_list
            self.accepted_street_types_list = accepted_street_types_list
            CurrentInputRow.__instance = self

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
        self.current_row_unit_no = current_row_unit_no

    @staticmethod
    def set_floor(self, current_row_floor):
        self.current_row_floor = current_row_floor

    @staticmethod
    def set_building(self, current_row_building):
        self.current_row_building = current_row_building

    @staticmethod
    def set_street(self, current_row_street):
        self.current_row_street = current_row_street

    @staticmethod
    def set_section(self, current_row_section):
        self.current_row_section = current_row_section

    @staticmethod
    def set_city(self, current_row_city):
        self.current_row_city = current_row_city

    @staticmethod
    def set_state(self, current_row_state):
        self.current_row_state = current_row_state

    @staticmethod
    def set_postcode(self, current_row_postcode):
        self.current_row_postcode = current_row_postcode

    @staticmethod
    def set_search_level_flag(self, current_row_search_level_flag):
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
    def get_created_at(self):
        return self.current_row_created_at

    @staticmethod
    def get_updated_at(self):
        return self.current_row_updated_at