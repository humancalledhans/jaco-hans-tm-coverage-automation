from abc import ABCMeta, abstractstaticmethod

class ICurrentInputRow(metaclass=ABCMeta):

	@abstractstaticmethod
	def get_input_header_data():
		""" to implement in child class """

	@abstractstaticmethod
	def get_input_row_data():
		""" to implement in child class """

	@abstractstaticmethod
	def set_input_header_data():
		""" to implement in child class """

	@abstractstaticmethod
	def set_input_row_data():
		""" to implement in child class """

	@abstractstaticmethod
	def set_accepted_states_list():
		""" to implement in child class """

	@abstractstaticmethod
	def set_accepted_street_types_list():
		""" to implement in child class """


	@abstractstaticmethod
	def get_accepted_states_list():
		""" to implement in child class """

	@abstractstaticmethod
	def get_accepted_street_types_list():
		""" to implement in child class """

	@abstractstaticmethod
	def get_house_unit_lotno():
		""" to implement in child class """

	@abstractstaticmethod
	def get_street_type():
		""" to implement in child class """

	@abstractstaticmethod
	def get_street_name():
		""" to implement in child class """

	@abstractstaticmethod
	def get_section():
		""" to implement in child class """

	@abstractstaticmethod
	def get_floor_no():
		""" to implement in child class """

	@abstractstaticmethod
	def get_building_name():
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
	def get_tid_option():
		""" to implement in child class """

	@abstractstaticmethod
	def get_source_option():
		""" to implement in child class """

	@abstractstaticmethod
	def get_uid():
		""" to implement in child class """

	@abstractstaticmethod
	def get_result_type():
		""" to implement in child class """

	@abstractstaticmethod
	def get_result_string():
		""" to implement in child class """

	@abstractstaticmethod
	def get_salesman():
		""" to implement in child class """

	@abstractstaticmethod
	def get_email_notification():
		""" to implement in child class """

	@abstractstaticmethod
	def get_telegram():
		""" to implement in child class """



class CurrentInputRow(ICurrentInputRow):

	__instance = None

	@staticmethod
	def get_instance():
		if CurrentInputRow.__instance is None:
			CurrentInputRow(input_header_data=None, input_row_data=None, accepted_states_list=None, accepted_street_types_list=None)
		return CurrentInputRow.__instance
	
	def __init__(self, input_header_data=None, input_row_data=None, accepted_states_list=None, accepted_street_types_list=None):
		if CurrentInputRow.__instance is not None:
			raise Exception("CurrentInputRow instance cannot be instantiated more than once!")
		else:
			self.input_header_data = input_header_data
			self.input_row_data = input_row_data
			self.accepted_states_list = accepted_states_list
			self.accepted_street_types_list = accepted_street_types_list
			CurrentInputRow.__instance = self

	@staticmethod
	def set_csv_file_path(self, csv_file_path):
		self.csv_file_path = csv_file_path

	@staticmethod
	def set_input_header_data(self, input_header_data):
		self.input_header_data = input_header_data

	@staticmethod
	def set_input_row_data(self, input_row_data):
		self.input_row_data = input_row_data

	@staticmethod
	def set_accepted_states_list(self, accepted_states_list):
		self.accepted_states_list = accepted_states_list

	@staticmethod
	def set_accepted_street_types_list(self, accepted_street_types_list):
		self.accepted_street_types_list = accepted_street_types_list


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
	def get_house_unit_lotno(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_house_unit_lotno_index = input_header_data.index('House/Unit/Lot No.')
		input_house_unit_lotno = input_row_data[input_house_unit_lotno_index]

		return input_house_unit_lotno

	@staticmethod
	def get_street_type(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_street_type_index = input_header_data.index('Street Type')
		input_street_type = input_row_data[input_street_type_index]

		return input_street_type

	@staticmethod
	def get_street_name(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_street_name_index = input_header_data.index('Street Name')
		input_street_name = input_row_data[input_street_name_index]

		return input_street_name

	@staticmethod
	def get_section(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_section_index = input_header_data.index('Section')
		input_section = input_row_data[input_section_index]

		return input_section

	@staticmethod
	def get_floor_no(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_floor_no_index = input_header_data.index('Floor No.')
		input_floor_no = input_row_data[input_floor_no_index]

		return input_floor_no

	@staticmethod
	def get_building_name(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_building_name_index = input_header_data.index('Building Name')
		input_building_name = input_row_data[input_building_name_index]

		return input_building_name

	@staticmethod
	def get_city(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_city_index = input_header_data.index('City')
		input_city = input_row_data[input_city_index]

		return input_city

	@staticmethod
	def get_state(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_state_index = input_header_data.index('State')
		input_state = input_row_data[input_state_index]

		return input_state

	@staticmethod
	def get_postcode(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_postcode_index = input_header_data.index('Postcode')
		input_postcode = input_row_data[input_postcode_index]

		return input_postcode

	@staticmethod
	def get_tid_option(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_tid_option_index = input_header_data.index('tid (option)')
		input_tid_option = input_row_data[input_tid_option_index]

		return input_tid_option

	@staticmethod
	def get_source_option(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_source_option_index = input_header_data.index('source (option)')
		input_source_option = input_row_data[input_source_option_index]
		
		return input_source_option

	@staticmethod
	def get_uid(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_uid_index = input_header_data.index('Uid')
		input_uid = input_row_data[input_uid_index]

		return input_uid

	@staticmethod
	def get_result_type(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_result_type_index = input_header_data.index('Result type')
		input_result_type = input_row_data[input_result_type_index]

		return input_result_type

	@staticmethod
	def get_result_string(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_result_string_index = input_header_data.index('result string')
		input_result_string = input_row_data[input_result_string_index]

		return input_result_string

	@staticmethod
	def get_salesman(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_salesman_index = input_header_data.index('Salesman')
		input_salesman = input_row_data[input_salesman_index]

		return input_salesman

	@staticmethod
	def get_email_notification(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_email_notification_index = input_header_data.index('Email Notification')
		input_email_notification = input_row_data[input_email_notification_index]

		return input_email_notification

	@staticmethod
	def get_telegram(self):
		input_header_data = self.get_input_header_data(self=self)
		input_row_data = self.get_input_row_data(self=self)

		input_telegram_index = input_header_data.index('telegram')
		input_telegram = input_row_data[input_telegram_index]

		return input_telegram



