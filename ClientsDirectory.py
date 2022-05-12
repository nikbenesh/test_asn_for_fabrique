from Client import Client
import sqlite3
import re
from DB import DB


# справочник с клиентами + база данных

class ClientsDB(DB):
	def __init__(self, db_file):
		DB.__init__(self, db_file)
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS clients(
			id integer, phone_number text, mobile_op_code integer, tag text, timezone text)''')

	def addClient(self, client):
		self.cursor.execute('INSERT INTO clients VALUES (?, ?, ?, ?, ?)', 
			(client.getID(), client.getPhone(), client.getOpCode(), client.getTag(), client.getTimezone()))
		self.connection.commit()

	def deleteClient(self, client_id):
		self.cursor.execute('DELETE FROM clients WHERE id = (?)', (str(client_id),))
		self.connection.commit()

	def getClientByID(self, client_id):
		return self.cursor.execute('SELECT * FROM clients WHERE id = (?)', (str(client_id),)).fetchone()

	def updateClientPhone(self, client_id, new_phone):
		if (re.search(r"7[\d]{10}", new_phone)):
			self.cursor.execute("UPDATE clients SET phone_number = ? WHERE id = ?", (new_phone, str(client_id)))
			self.connection.commit()

	def updateClientOpCode(self, client_id, new_code):
		self.cursor.execute("UPDATE clients SET mobile_op_code = ? WHERE id = ?", (new_code, str(client_id)))
		self.connection.commit()

	def updateClientTag(self, client_id, new_tag):
		self.cursor.execute("UPDATE clients SET tag = ? WHERE id = ?", (new_tag, str(client_id)))
		self.connection.commit()

	def updateClientTimezone(self, client_id, new_tz):
		self.cursor.execute("UPDATE clients SET timezone = ? WHERE id = ?", (new_tz, str(client_id)))
		self.connection.commit()

	def getClients(self, query=""):
		if (query):
			query = "SELECT * FROM clients WHERE " + query
		query = "SELECT * FROM clients"
		return [Client(el[1], el[2], el[3], el[4], id=el[0]) for el in self.cursor.execute(query).fetchall()]
