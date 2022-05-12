# рассылка

from Message import Message
from ClientsDirectory import ClientsDB
from datetime import datetime
import asyncio
from IDGenerator import generateID


class MailingList:
	def __init__(self, message_text, ending_date, start_date=datetime.now(), clients_filter_query=""):
		self.id = generateID()
		self.message_text = message_text
		self.clients_filter_query = clients_filter_query
		self.ending_date = ending_date
		self.start_date = start_date
		self.clients_db = ClientsDB('clients.db')

	async def launch(self):
		# time_to_sleep = (self.start_date - datetime.now()).seconds
		# print('starting at', self.start_date)
		# print('now is', datetime.now())
		# print('diff is', self.start_date - datetime.now())
		# print('will wait for', time_to_sleep)
		if (self.start_date > datetime.now()):
			await asyncio.sleep((self.start_date - datetime.now()).seconds)
		successful_msgs = 0
		failed_msgs = 0
		for client in self.clients_db.getClients(self.clients_filter_query):
			# if (datetime.now(tz=client.getTimezone()) < self.ending_date):
			msg = Message(self.id, client.getID(), client.getPhone(), self.message_text)
			print('sending a message to client', client.getID())
			status = msg.send()
			if (status == 0):
				successful_msgs += 1
			else:
				failed_msgs += 1
		print('Success:', successful_msgs, 'Failure:', failed_msgs)
		return (successful_msgs, failed_msgs)

	def getID(self):
		return self.id

	def getMsg(self):
		return self.message_text

	def setMsg(self, msg):
		self.message_text = msg

	def getQuery(self):
		return self.clients_filter_query

	def setQuery(self, query):
		self.clients_filter_query = query

	def getStartDate(self):
		return self.start_date

	def setStartDate(self, date):
		self.start_date = date

	def getEndDate(self):
		return self.ending_date

	def setEndDate(self, date):
		self.ending_date = date

