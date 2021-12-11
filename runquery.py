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

	def insertExpense(self, source, cost, category, account, details, date):
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

		# get balance as a string and remove '$'
		balance = cursor.fetchall()[0][0].replace('$','')
		try:
			balance = float(balance)
		# else change to a foat
		except:	
			balance = float(balance.replace(',',''))

		# update credit loan balances
		if category == 'mines loan' or category == 'america first car loan':
			# dict for each account name and id
			loanAccounts = {'mines loan': 13, 'america first car loan': 12}
			loanId = loanAccounts[category]

			# query balance of loan
			loanQuery = "SELECT balance FROM finance_accounts WHERE account_id = %s"
			cursor.execute(loanQuery, [loandId,])
			loanBalance = cursor.fetchall()[0][0]

			# calculate remaining balance after cost applied
			if loanId == 13:
				# interest paid
				interest = balance * (12/0.45)
				# principle paid
				principle = cost - interest
				newBalance = loanBalance - principle

			elif loanId == 12:
				newBalance = loanBalance - cost

			# update account
			loanQuery = "UPDATE finance_accounts SET balance = %s WHERE account_id = %s"
			cursor.execute(loanQuery, [newBalance, loanId])

			# update account history
			query = "INSERT INTO finance_account_history (account_id, balance, dt, expense_id) VALUES (%s, %s, %s, %s)"
			cursor.execute(query, [loandId, newBalance, date, expenseId])


		# subtract cost from balance and insert into finance history table
		newBalance = balance - cost
		query = "INSERT INTO finance_account_history (account_id, balance, dt, expense_id) VALUES (%s, %s, %s, %s)"
		cursor.execute(query, [accountId, newBalance, date, expenseId])

		# update account balance
		query = "UPDATE finance_accounts SET balance = %s WHERE account_id = %s"
		cursor.execute(query, [newBalance, accountId])

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

	def transferUpdate(self, source, money, category, account, details, date):
		cursor, connection = self.createConnection()

		# select account id from source and receive account
		srcIdQuery = "SELECT account_id FROM finance_accounts WHERE account = %s"
		cursor.execute(srcIdQuery, [source,])
		sourceId = int(cursor.fetchall()[0][0])

		rcvIdQuery = "SELECT account_id FROM finance_accounts WHERE account = %s"
		cursor.execute(rcvIdQuery, [account,])
		receiveId = int(cursor.fetchall()[0][0])

		# select amount from source account
		sourceQuery = "SELECT balance FROM finance_accounts WHERE account = %s"
		cursor.execute(sourceQuery, [source,])
		# remove dollar sign from result and cast as a float
		sourceBalance = float(cursor.fetchall()[0][0].replace('$', ''))

		# select amount from receiving account
		receiveQuery = "SELECT balance FROM finance_accounts WHERE account = %s"
		cursor.execute(receiveQuery, [account,])
		receiveBalance = float(cursor.fetchall()[0][0].replace('$', ''))

		# update source account with difference of balance and money
		sourceBalance -= money
		sourceUpdate = "UPDATE finance_accounts SET balance = %s WHERE account = %s"
		cursor.execute(sourceUpdate, [sourceBalance, source])

		# update receive account with sum of balance and money
		receiveBalance += money
		receiveUpdate = "UPDATE finance_accounts SET balance = %s WHERE account = %s"
		cursor.execute(receiveUpdate, [receiveBalance, account])

		# insert new value into monthly transfers table
		insertTransfer = "INSERT INTO  transfers(amount, from_id, to_id, details, dt) VALUES (%s, %s, %s, %s, %s) RETURNING id"
		cursor.execute(insertTransfer, [money, sourceId, receiveId, details, date])
		transferId = int(cursor.fetchone()[0])

		# update finance account history with new balance for source and receive table
		updatedBalance = [sourceId, sourceBalance, date, transferId]
		query = "INSERT INTO finance_account_history (account_id, balance, dt, transfer_id) VALUES (%s, %s, %s, %s)"
		cursor.execute(query, updatedBalance)

		updatedBalance = [receiveId, receiveBalance, date, transferId]
		query = "INSERT INTO finance_account_history (account_id, balance, dt, transfer_id) VALUES (%s, %s, %s, %s)"
		cursor.execute(query, updatedBalance)

		self.closeConnection(cursor, connection)
