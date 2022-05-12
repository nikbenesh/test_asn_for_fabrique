from datetime import datetime
import requests
from IDGenerator import generateID


ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODI1MzAxMjEsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Im5pY2V0YXNfYiJ9.b35umo8oVexOvfcwBYMKZXdj7hIeBq0Aut707DTDsiQ'

class Message:
	def __init__(self, mailing_list_id, client_id, client_phone, msg_text):
		self.mailing_list_id = mailing_list_id
		self.client_id = client_id
		self.id = generateID()
		self.msg_text = msg_text
		self.client_phone = client_phone

	def send(self):
		link = "https://probe.fbrq.cloud/v1/send/" + str(self.id)
		msg_obj = {'id': self.client_id, 'phone': self.client_phone, 'text': self.msg_text}
		self.sending_date = datetime.now()
		response = requests.post(link, headers={'Authorization': ACCESS_TOKEN, 'Content-Type': 'application/json'}, data=msg_obj)
		# if (response.status_code == 200) and (response.headers['content-type'] == 'application/json') and 
		# ('code' in response.json()):
		# 	self.status = response.json()['code']
		# else:
		# 	self.status = -2
		try:
			self.status = response.json()['code']
		except requests.exceptions.JSONDecodeError as e:
			print(e)
			self.status = -2
		return self.status

