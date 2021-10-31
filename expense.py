from datetime import datetime
from runquery import RunQuery

class Expense:
	"""a class for organizing all expenses of financial records"""

	def __init__(self, vendor, cost, category, paymentType, date):
		"""Initialize expense attributes"""
		self.vendor = vendor
		self.cost = cost
		self.category = category
		self.paymentType = paymentType
		if date == None:
			self.date = datetime.now().strftime('%Y-%m-%d')
		else:
			self.date = date
	def getExpenses():
		"""Show expenses for the current month"""

		print("in the works")

	def setExpense(self):
		connect = RunQuery('finances', 'localhost')
		connect.insertExpense(self.vendor, self.cost, self.category, self.paymentType, self.date)