from IDGenerator import generateID
import re


class Client:
	def __init__(self, phone_number, mobile_op_code, tag, timezone, id=0):
		if (self.validPhone(phone_number)):
			self.phone_number = phone_number
		self.mobile_op_code = mobile_op_code
		self.tag = tag
		self.timezone = timezone
		if (id == 0):
			self.id = generateID()
		else:
			self.id = id

	def validPhone(self, phone):
		return re.search(r"7[\d]{10}", phone)

	def getPhone(self):
		return self.phone_number

	def getOpCode(self):
		return self.mobile_op_code

	def getTag(self):
		return self.tag

	def getTimezone(self):
		return self.timezone

	def getID(self):
		return self.id