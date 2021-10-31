import psycopg2
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
		# connect to finances db, monthly_expenses table
		conn = psycopg2.connect(dbname = "finances", host = "localhost")
		cursor = conn.cursor()
		query  = "INSERT INTO monthly_expenses (vendor, cost, category, payment_type, dt) VALUES (%s, %s, %s, %s, %s)"

		singleExpense = [self.expense, self.cost, self.details, self.payment, self.date]
		cursor.execute(query, singleExpense)

		conn.commit()
		cursor.close()
		conn.close()