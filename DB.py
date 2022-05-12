import sqlite3


class DB:
	def __init__(self, db_file):
		self.file = db_file
		self.connection = sqlite3.connect(self.file)
		self.cursor = self.connection.cursor()