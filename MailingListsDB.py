import sqlite3
from datetime import datetime
import asyncio
from MailingList import MailingList
from DB import DB


class MailingListsDB(DB):
	def __init__(self, db_file):
		DB.__init__(self, db_file)
		self.active_lists = []
		self.tasks = []
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS mailing_lists(
			id integer, msg_text text, start_date date, end_date date, successful_msgs integer, failed_msgs integer)''')

	async def _startMailingList_(self, mailing_list):
		mailing_list_task = asyncio.create_task(mailing_list.launch())
		el = (mailing_list_task, mailing_list.getID())
		self.active_lists.append(mailing_list)
		self.tasks.append(el)
		successful_msgs, failed_msgs = (await asyncio.gather(mailing_list_task))[0]
		self.cursor.execute('UPDATE mailing_lists SET successful_msgs = ?, failed_msgs = ? WHERE id = ?', 
			(successful_msgs, failed_msgs, mailing_list.getID()))
		self.active_lists.remove(mailing_list)
		self.tasks.remove(el)

	def startMailingList(self, mailing_list):
		asyncio.run(self._startMailingList_(mailing_list))

	def addList(self, mailing_list):
		self.cursor.execute('INSERT INTO mailing_lists VALUES (?, ?, ?, ?, 0, 0)', 
			(mailing_list.getID(), mailing_list.getMsg(), mailing_list.getStartDate(), mailing_list.getEndDate()))
		self.connection.commit()
		self.startMailingList(mailing_list)

	def deleteList(self, mailing_list_id):
		self.cancelList(mailing_list_id)
		self.cursor.execute('DELETE FROM mailing_lists WHERE id = (?)', str(mailing_list_id))
		self.connection.commit()

	def findActiveList(self, mailing_list_id):
		for el in active_lists:
			if (el.getID() == mailing_list_id):
				return el
		print('Не найдена незавершенная рассылка с id:', mailing_list_id)
		return -1

	def cancelList(self, mailing_list_id):
		mailing_list = self.findActiveList(mailing_list_id)
		if (mailing_list == -1):
			return -1

		for task in self.tasks:
			if (task[1] == mailing_list_id):
				task[0].cancel()
				self.tasks.remove(task)
		self.active_lists.remove(mailing_list)
		return mailing_list

	def updateListStartDate(self, mailing_list_id, new_date):
		mailing_list = self.cancelList(mailing_list_id)
		if (mailing_list == -1):
			print('Невозможно изменить параметры рассылки, так как она уже завершена')
			return -1
		mailing_list.setStartDate(new_date)
		self.cursor.execute("UPDATE mailing_lists SET start_date = ? WHERE id = ?", (new_date, str(mailing_list_id)))
		self.connection.commit()
		self.startMailingList(mailing_list)
		return 1

	def updateListEndDate(self, mailing_list_id, new_date):
		mailing_list = self.cancelList(mailing_list_id)
		if (mailing_list == -1):
			print('Невозможно изменить параметры рассылки, так как она уже завершена')
			return -1
		mailing_list.setEndDate(new_date)
		self.cursor.execute("UPDATE mailing_lists SET end_date = ? WHERE id = ?", (new_date, str(mailing_list_id)))
		self.connection.commit()
		self.startMailingList(mailing_list)
		return 1

	def updateListMsg(self, mailing_list_id, msg):
		mailing_list = self.cancelList(mailing_list_id)
		if (mailing_list == -1):
			print('Невозможно изменить параметры рассылки, так как она уже завершена')
			return -1
		mailing_list.setMsg(msg)
		self.cursor.execute("UPDATE mailing_lists SET msg_text = ? WHERE id = ?", (msg, str(mailing_list_id)))
		self.connection.commit()
		self.startMailingList(mailing_list)
		return 1

	def updateListQuery(self, mailing_list_id, query):
		mailing_list = self.cancelList(mailing_list_id)
		if (mailing_list == -1):
			print('Невозможно изменить параметры рассылки, так как она уже завершена')
			return -1
		mailing_list.setQuery(query)
		self.startMailingList(mailing_list)
		return 1

	def getActiveLists(self):
		return self.active_lists

	def showGeneralStats(self):
		mailing_lists = self.cursor.execute('SELECT * FROM mailing_lists').fetchall()
		for mailing_list in mailing_lists:
			print("ID: %d\n Message text: %s\n Start date: %s\n End date: %s\n Successful Messages: %d\n Failed Messages: %d\n" % tuple(mailing_list))


	def getMailingListStats(self, mailing_list_id):
		mailing_list = self.cursor.execute('SELECT * FROM mailing_lists WHERE id = (?)', (str(mailing_list_id),)).fetchone()
		print("ID: %d\n Message text: %s\n Start date: %s\n End date: %s\n Successful Messages: %d\n Failed Messages: %d\n" % tuple(mailing_list))



