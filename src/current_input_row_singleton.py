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


class CurrentInputRow(ICurrentInputRow):

	__instance = None

	@staticmethod
	def get_instance():
		if CurrentInputRow.__instance is None:
			CurrentInputRow(input_header_data=None, input_row_data=None)
		return CurrentInputRow.__instance
	
	def __init__(self, input_header_data=None, input_row_data=None):
		if CurrentInputRow.__instance is not None:
			raise Exception("Singleton cannot be instantiated more than once!")
		else:
			self.input_header_data = input_header_data
			self.input_row_data = input_row_data
			CurrentInputRow.__instance = self

	@staticmethod
	def get_input_header_data(self):
		return self.input_header_data

	@staticmethod
	def get_input_row_data(self):
		return self.input_row_data

	@staticmethod
	def set_input_header_data(self, input_header_data):
		self.input_header_data = input_header_data

	@staticmethod
	def set_input_row_data(self, input_row_data):
		self.input_row_data = input_row_data