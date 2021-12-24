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

	def selectQuery(self, cursor, table, search, arguments, columns = "*"):
		queryString = f"SELECT {columns} FROM {table} WHERE {search} = %s"
		cursor.execute(queryString, arguments)

		if columns == "*":
			results = cursor.fetchall()
		else:
			results = cursor.fetchall()[0][0]

		return results
		
	def insertQuery(self, cursor, table, columns, values, returnValue=""):
		# make a tuple of %s placeholders that is same size as values list
		placeArgs = str(tuple(["%s"]*len(values))).replace("'","")
		insertQuery = f"INSERT INTO {table}{columns} VALUES {placeArgs} {returnValue}"
		cursor.execute(insertQuery, values)

		# only return results if returnValue is passed into function
		if returnValue != "":
			return cursor.fetchone()[0]

	def updateQuery(self, cursor, table, setArg, whereArg, params):
		loanQuery = f"UPDATE {table} SET {setArg} = %s WHERE {whereArg} = %s"
		cursor.execute(loanQuery, params)


	def insertExpense(self, source, cost, category, account, details, date):
		cursor, connection = self.createConnection()

		# check if current expense category and account already exist by checking length of returned result
		categoryResults = self.selectQuery(cursor, "expense_categories", "expense_category",[category,])
		accountResults = self.selectQuery(cursor, "finance_accounts", "account", [account,])

		# if category or account don't exist insert into tables, else get existing ids
		if len(categoryResults) == 0:
			categoryId = self.insertQuery(cursor, "(expense_categories)", "expense_category", [category,], "RETURNING category_id")
		else:
			categoryId = self.selectQuery(cursor, "expense_categories", "expense_category", [category,], "category_id")

		if len(accountResults) == 0:
			accountId = self.insertQuery(cursor, "finance_accounts", "(account)", [account,], "RETURNING account_id")
		else:
			accountId = self.selectQuery(cursor, "finance_accounts", "(account)", [account,], "account_id")

		# insert expense into the table
		expenseValues = [source, cost, categoryId, accountId, details, date]
		expenseColumns = "(vendor, cost, category_id, account_id, details, dt)"
		expenseId = self.insertQuery(cursor, "monthly_expenses", expenseColumns, expenseValues, "RETURNING expense_id")

		# query account balance
		balance = self.selectQuery(cursor, "finance_accounts", "account_id", [accountId,], "balance").replace('$','')		
		# convert to a float if no apostrophe in balance
		try:
			balance = float(balance)
		except:	
			balance = float(balance.replace(',',''))

		# update loan balances
		if category == 'mines loan' or category == 'america first car loan':
			# dict for each account name and id
			loanAccounts = {'mines loan': 13, 'america first car loan': 12}
			loanId = loanAccounts[category]

			# query balance of loan
			loanBalance = self.selectQuery(cursor, "finance_accounts", "account_id", [loanId,], "balance")

			# calculate remaining balance after cost applied
			if loanId == 13:
				# interest paid
				interest = balance * (12/0.045)
				# principal paid
				principle = cost - interest
				newBalance = loanBalance - principle

			elif loanId == 12:
				newBalance = loanBalance - cost

			# update credit account with new balance
			self.updateQuery(cursor, "finance_accounts", "balance", "account_id", [newBalance, loanId])

			# update account history with a record of new balance
			historyValues = [loandId, newBalance, date, expenseId]
			historyColumns = "(account_id, balance, dt, expense_id)"
			self.insertQuery(cursor, "finance_account_history", historyColumns, historyValues)

		# subtract cost from balance and insert into finance history table
		newBalance = balance - cost
		historyColumns = "(account_id, balance, dt, expense_id)"
		historyValues = [accountId, newBalance, date, expenseId]
		self.insertQuery(cursor, "finance_account_history", historyColumns, historyValues)

		# update account balance
		self.updateQuery(cursor, "finance_accounts", "balance", "account_id", [newBalance, accountId])

		self.closeConnection(cursor, connection)

	def insertIncome(self, source, income, category, account, date):
		cursor, connection = self.createConnection()

		# checkAccount = "SELECT * FROM finance_accounts WHERE account = %s"
		# cursor.execute(checkAccount, [account,])
		# accountResults = cursor.fetchall()
		# cursor, table, search, arguments, columns = "*"
		accountResults = self.selectQuery(cursor, "finance_accounts", "account", [account,])

		if accountResults == 0:
			# cursor, table, columns, values, returnValue=""
			# insertAccount = "INSERT INTO finance_accounts (account) VALUES (%s) RETURNING account_id"
			# cursor.execute(query, [account,])
			# accountId = cursor.fetchone()[0]
			accountId = self.insertQuery(cursor, "finance_accounts", "(account)", [account,], "RETURNING account_id")
		else:
			# query = "SELECT account_id FROM finance_accounts WHERE account = %s"
			# cursor.execute(query, [account,])
			# accountId = cursor.fetchall()[0][0]
			accountId = self.selectQuery(cursor, "finance_accounts", "account", [account,], "account_id")

		incomeAdd = [source, income, category, accountId, date]
		incomeColumns = "(source, income, income_category, account_id, dt)"
		# query = "INSERT INTO " + self.table + " (source, income, income_category, account_id, dt) VALUES (%s, %s, %s, %s, %s) RETURNING income_id"
		# cursor.execute(query, incomeAdd)
		# incomeId = cursor.fetchone()[0]
		incomeId = self.insertQuery(cursor, "monthly_income", incomeColumns, incomeAdd, "RETURNING income_id")

		# query account balance
		# query = "SELECT balance FROM finance_accounts WHERE account_id = %s"
		# cursor.execute(query, [accountId,])
		# remove dollar sign from result and cast as a float
		balance = self.selectQuery(cursor, "finance_accounts", "account_id", [accountId,], "balance").replace('$', '')

		try:
			balance = float(balance)
		except:	
			balance = float(balance.replace(',',''))

		# subtract cost from balance and insert into finance history table
		newBalance = balance + income
		# updatedBalance = [accountId, newBalance, date, incomeId]
		# query = "INSERT INTO finance_account_history (account_id, balance, dt, income_id) VALUES (%s, %s, %s, %s)"
		# cursor.execute(query, updatedBalance)
		historyColumns = "(account_id, balance, dt, income_id)"
		historyValues = [accountId, newBalance, date, incomeId]
		self.insertQuery(cursor, "finance_account_history", historyColumns, historyValues)

		# update account balance
		currentBalance = [newBalance, accountId]
		query = "UPDATE finance_accounts SET balance = %s WHERE account_id = %s"
		cursor.execute(query, currentBalance)
		# cursor, table, setArg, whereArg, params
		self.updateQuery(cursor, "finance_accounts", "balance", "account_id", [newBalance, accountId])

		self.closeConnection(cursor, connection)

	def transferUpdate(self, source, money, category, account, details, date):
		cursor, connection = self.createConnection()

		# select account id from source and receive account
		sourceId = int(self.selectQuery(cursor, "finance_accounts", "account", [source,], "account_id"))
		receiveId = int(self.selectQuery(cursor, "finance_accounts", "account", [account,], "account_id"))

		# select amount from source account
		sourceBalance = self.selectQuery(cursor, "finance_accounts", "account", [source,], "balance").replace("$","")

		try:
			sourceBalance = float(sourceBalance)
		except:	
			sourceBalance = float(sourceBalance.replace(',',''))

		# select amount from receiving account
		receiveBalance = self.selectQuery(cursor, "finance_accounts", "account", [account,], "balance").replace("$","")
		
		try:
			receiveBalance = float(receiveBalance)
		except:	
			receiveBalance = float(receiveBalance.replace(',',''))

		# update source account with difference of balance and money
		sourceBalance -= money
		self.updateQuery(cursor, "finance_accounts", "balance", "account", [sourceBalance, source])

		# update receive account with sum of balance and money
		receiveBalance += money
		self.updateQuery(cursor, "finance_accounts", "balance", "account", [receiveBalance, account])

		# insert new value into transfers table
		transferColumns = "(amount, from_id, to_id, details, dt)"
		transferValues = [money, sourceId, receiveId, details, date]
		transferId = int(self.insertQuery(cursor, "transfers", transferColumns, transferValues, "RETURNING id"))

		# update balance in account w/ removed balance
		historyColumns = "(account_id, balance, dt, transfer_id)"
		historyValues = [sourceId, sourceBalance, date, transferId]
		self.insertQuery(cursor, "finance_account_history", historyColumns, historyValues)

		# update balance in account that received money
		historyValues = [receiveId, receiveBalance, date, transferId]
		self.insertQuery(cursor, "finance_account_history", historyColumns, historyValues)

		self.closeConnection(cursor, connection)