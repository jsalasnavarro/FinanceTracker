import mysql.connector
from datetime import datetime

class Expense:
	"""a class for organizing all expenses of financial records"""

	def __init__(self, expense, cost, details, payment, date, password):
		"""Initialize expense attributes"""
		self.expense = expense
		self.cost = cost
		self.details = details
		self.payment = payment
		self.date = datetime.now().strftime('%Y-%m-%d')
		self.password = password

	def getExpenses():
		"""Print all expenses for the current month"""

		print("in the works")

	def setExpense(self):
		# connect to finance db, expenses table
		financeDB = mysql.connector.connect(
			host = "localhost",
			port = "3306",
			user = "root",
			database = "finance",
			password = self.password)

		cursor = financeDB.cursor()
		query  = "INSERT INTO expenses (expense, cost, details, payment, dt) VALUES (%s, %s, %s, %s, %s)"
		singleExpense = [self.expense, self.cost, self.details, self.payment, self.date]
		cursor.execute(query, singleExpense)

		financeDB.commit()
		cursor.close()
		financeDB.close()