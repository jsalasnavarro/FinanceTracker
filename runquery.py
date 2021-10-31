import psycopg2

class RunQuery:
	def __init__(self, name, host):
		self.name = name
		self.host = host

	def createConnection(self):
		# connect to db 'name'
		connection = psycopg2.connect(dbname = self.name, host = self.host)
		cursor = connection.cursor()
		return cursor, connection

	def closeConnection(self, cursor, connection):
		connection.commit()
		cursor.close()
		connection.close()

	def insertExpense(self, vendor, cost, category, paymentType, date):
		cursor, connection = self.createConnection()

		expense = [vendor, cost, category, paymentType, date]
		query  = "INSERT INTO monthly_expenses (vendor, cost, category, payment_type, dt) VALUES (%s, %s, %s, %s, %s)"
		cursor.execute(query, expense)

		self.closeConnection(cursor, connection)