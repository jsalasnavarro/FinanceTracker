from datetime import datetime
from runquery import RunQuery

class Finance:
	"""a class for organizing all expenses of financial records"""
	def __init__(self):
		self.db = "finances"
		self.host = "localhost"
			
	def getMonthExpenses():
		"""show expenses for the current month"""
		print("in the works")

	def setExpense(self, source, money, category, account, date=datetime.now().strftime('%Y-%m-%d'), details = ""):
		# table, database, server
		connect = RunQuery(self.db, self.host)
		connect.insertExpense(source, money, category, account, details, date)

	def setIncome(self, source, money, category, account, date=datetime.now().strftime('%Y-%m-%d')):
		# table, database, server
		connect = RunQuery(self.db, self.host)
		connect.insertIncome(source, money, category, account, date)

	def transferFunds(self, source, money, account, date=datetime.now().strftime('%Y-%m-%d'), details = ""):
		# table, database, server
		connect = RunQuery(self.db, self.host)
		# source is where money is sent to
		# account is account money is leaving from
		connect.transferUpdate(source, money, account, details, date)

	def deleteValue(self, id):
		connect = RunQuery(self.db, self.host)
		connect.deleteExpense(datetime.now().strftime('%Y-%m-%d'), id)