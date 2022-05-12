from MailingListsDB import MailingListsDB
from MailingList import MailingList
from ClientsDirectory import ClientsDB
from datetime import datetime


mdb = MailingListsDB('mailing_lists.db')
cdb = ClientsDB('clients.db')

mdb.addList(MailingList('hi', datetime(2022, 5, 1)))
mdb.showGeneralStats()


