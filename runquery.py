import psycopg2

class RunQuery:
	def __init__(self, table, database, host):
		self.table = table
		self.database = database
		self.host = host

	def createConnection(self):
		# connect to db 'name'
		connection = psycopg2.connect(dbname = self.database, host = self.host)
		cursor = connection.cursor()
		return cursor, connection

	def closeConnection(self, cursor, connection):
		connection.commit()
		cursor.close()
		connection.close()

	def insertExpense(self, source, cost, category, account, date):
		cursor, connection = self.createConnection()

		expense = [source, cost, category, account, date]
		query = "INSERT INTO " + self.table + " (vendor, cost, category, account, dt) VALUES (%s, %s, %s, %s, %s)"
		cursor.execute(query, expense)

		self.closeConnection(cursor, connection)

	def insertIncome(self, source, income, category, account, date):
		cursor, connection = self.createConnection()

		income = [source, income, category, account, date]
		query = "INSERT INTO " + self.table + " (source, income, category, account, dt) VALUES (%s, %s, %s, %s, %s)"
		cursor.execute(query, income)

		self.closeConnection(cursor, connection)
		