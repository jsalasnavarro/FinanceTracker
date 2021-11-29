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

	def insertExpense(self, source, cost, category, account,details, date):
		cursor, connection = self.createConnection()

		# query category and account
		checkCategory = "SELECT * FROM expense_categories WHERE expense_category = %s"
		cursor.execute(checkCategory, [category,])
		categoryResults = cursor.fetchall()

		checkAccount = "SELECT * FROM finance_accounts WHERE account = %s"
		cursor.execute(checkAccount, [account,])
		accountResults = cursor.fetchall()

		# if category or account don't exist insert into tables, else get existing ids
		if len(categoryResults) == 0:
			insertCategory = "INSERT INTO expense_categories(expense_category) VALUES (%s) RETURNING category_id"
			cursor.execute(insertCategory, [category,])
			categoryId = cursor.fetchone()[0]
		else:
			query = "SELECT category_id FROM expense_categories WHERE expense_category = %s"
			cursor.execute(query, [category,])
			categoryId = cursor.fetchall()[0][0]

		if len(accountResults) == 0:
			insertAccount = "INSERT INTO finance_accounts (account) VALUES (%s) RETURNING account_id"
			cursor.execute(insertAccount, [account,])
			accountId = cursor.fetchone()[0]
		else:
			query = "SELECT account_id FROM finance_accounts WHERE account = %s"
			cursor.execute(query, [account,])
			accountId = cursor.fetchall()[0][0]

		# insert expense into the table
		expense = [source, cost, categoryId, accountId, details, date]
		query = "INSERT INTO " + self.table + " (vendor, cost, category_id, account_id, details, dt) VALUES (%s,%s, %s, %s, %s, %s) \n RETURNING expense_id"
		cursor.execute(query, expense)
		expenseId = cursor.fetchone()[0]

		# query account balance
		query = "SELECT balance FROM finance_accounts WHERE account_id = %s"
		cursor.execute(query, [accountId,])
		# remove dollar sign from result and cast as a float
		balance = float(cursor.fetchall()[0][0].replace('$', ''))

		# subtract cost from balance and insert into finance history table
		newBalance = balance - cost
		updatedBalance = [accountId, newBalance, date, expenseId]
		query = "INSERT INTO finance_account_history (account_id, balance, dt, expense_id) VALUES (%s, %s, %s, %s)"
		cursor.execute(query, updatedBalance)

		# update account balance
		currentBalance = [newBalance, accountId]
		query = "UPDATE finance_accounts SET balance = %s WHERE account_id = %s"
		cursor.execute(query, currentBalance)

		self.closeConnection(cursor, connection)

	def insertIncome(self, source, income, category, account, date):
		cursor, connection = self.createConnection()

		checkAccount = "SELECT * FROM finance_accounts WHERE account = %s"
		cursor.execute(checkAccount, [account,])
		accountResults = cursor.fetchall()

		if accountResults == 0:
			insertAccount = "INSERT INTO finance_accounts (account) VALUES (%s) RETURNING account_id"
			cursor.execute(query, [account,])
			accountId = cursor.fetchone()[0]
		else:
			query = "SELECT account_id FROM finance_accounts WHERE account = %s"
			cursor.execute(query, [account,])
			accountId = cursor.fetchall()[0][0]

		incomeAdd = [source, income, category, accountId, date]
		query = "INSERT INTO " + self.table + " (source, income, income_category, account_id, dt) VALUES (%s, %s, %s, %s, %s) RETURNING income_id"
		cursor.execute(query, incomeAdd)
		incomeId = cursor.fetchone()[0]

		# query account balance
		query = "SELECT balance FROM finance_accounts WHERE account_id = %s"
		cursor.execute(query, [accountId,])
		# remove dollar sign from result and cast as a float
		balance = float(cursor.fetchall()[0][0].replace('$', ''))

		# subtract cost from balance and insert into finance history table
		newBalance = balance + income
		updatedBalance = [accountId, newBalance, date, incomeId]
		query = "INSERT INTO finance_account_history (account_id, balance, dt, income_id) VALUES (%s, %s, %s, %s)"
		cursor.execute(query, updatedBalance)

		# update account balance
		currentBalance = [newBalance, accountId]
		query = "UPDATE finance_accounts SET balance = %s WHERE account_id = %s"
		cursor.execute(query, currentBalance)

		self.closeConnection(cursor, connection)
		