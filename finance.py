from datetime import datetime
from runquery import RunQuery

class Finance:
	"""a class for organizing all expenses of financial records"""
	# source, money, category, account, date
	def __init__(self, table, source, money, category, account, date):
		"""Initialize expense attributes"""
		# source of income or expense
		self.table = table
		self.source = source
		self.money = money
		self.category = category
		self.account = account
		self.date = date
			
	def getMonthExpenses():
		"""show expenses for the current month"""
		print("in the works")

	def setExpense(self):
		connect = RunQuery(self.table, 'finances', 'localhost')
		connect.insertExpense( self.source, self.money, self.category, self.account, self.date)

	def setIncome(self):
		"""function to add income"""
		connect = RunQuery(self.table, 'finances', 'localhost')
		connect.insertIncome(self.source, self.money, self.category, self.account, self.date)	