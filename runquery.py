import psycopg2

class RunQuery:
	def __init__(self, database, host):
		"""initialize name of tables being used in class"""
		self.database = database
		self.host = host
		self.fa = "finance_accounts"
		self.fah = "finance_account_history"
		self.me = "monthly_expenses"
		self.mi = "monthly_income"
		self.ec = "expense_categories"
		self.transfers = "transfers"

	def createConnection(self):
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

	def deleteQuery(self, cursor, table, search, params):
		deleteQuery = f"DELETE FROM {table} WHERE {search} = %s"
		cursor.execute(deleteQuery, params)

	def convertDollars(self, amount):
		amount = amount.replace("$", "")
		if amount.find(",") == -1:
			# ',' not found
			amount = float(amount)
		else:
			# ',' found
			amount = float(amount.replace(",",""))
		return amount

	def updateLoanBalance(self, cursor, cost, balance, accountId, expenseId, date):
		# dict for each account name and id
		loanAccounts = {'mines loan': 13, 'america first car loan': 12}
		loanId = loanAccounts[category]

		# query balance of loan
		loanBalance = self.convertDollars(self.selectQuery(cursor, self.fa, "account_id", [loanId,], "balance"))

		# calculate remaining balance after cost applied
		if loanId == 13:
			# interest paid
			interest = balance * (12/0.045)
			# principal paid
			principal = cost - interest
			newBalance = loanBalance - principal

		elif loanId == 12:
			newBalance = loanBalance - cost

		# update credit account with new balance
		self.updateQuery(cursor, self.fa, "balance", "account_id", [newBalance, loanId])
		# update account history with a record of new balance
		historyValues = [loandId, newBalance, date, expenseId]
		historyColumns = "(account_id, balance, dt, expense_id)"
		self.insertQuery(cursor, self.fah, historyColumns, historyValues)

	def insertExpense(self, source, cost, category, account, details, date):
		cursor, connection = self.createConnection()

		# check if current expense category and account already exist by checking length of returned result
		categoryResults = self.selectQuery(cursor, self.ec, "expense_category",[category,])
		accountResults = self.selectQuery(cursor, self.fa, "account", [account,])

		# if category or account don't exist insert into tables, else get existing ids
		if len(categoryResults) == 0:
			categoryId = self.insertQuery(cursor, "(expense_categories)", "expense_category", [category,], "RETURNING category_id")
		else:
			categoryId = self.selectQuery(cursor, self.ec, "expense_category", [category,], "category_id")

		if len(accountResults) == 0:
			accountId = self.insertQuery(cursor, self.fa, "(account)", [account,], "RETURNING account_id")
		else:
			accountId = self.selectQuery(cursor, self.fa, "(account)", [account,], "account_id")

		# insert expense into the table
		expenseValues = [source, cost, categoryId, accountId, details, date]
		expenseColumns = "(vendor, cost, category_id, account_id, details, dt)"
		expenseId = self.insertQuery(cursor, self.me, expenseColumns, expenseValues, "RETURNING expense_id")

		# query account balance
		balance = self.convertDollars(self.selectQuery(cursor, self.fa, "account_id", [accountId,], "balance"))

		# update loan balances
		if category == "mines loan" or category == "america first car loan":
			self.updateLoanBalance(cursor, cost, balance, accountId, expenseId, date)

		# subtract cost from balance and insert into finance history table
		newBalance = balance - cost
		historyColumns = "(account_id, balance, dt, expense_id)"
		historyValues = [accountId, newBalance, date, expenseId]
		self.insertQuery(cursor, self.fah, historyColumns, historyValues)
		self.updateQuery(cursor, self.fa, "balance", "account_id", [newBalance, accountId])

		self.closeConnection(cursor, connection)

	def insertIncome(self, source, income, category, account, date):
		cursor, connection = self.createConnection()
		accountResults = self.selectQuery(cursor, self.fa, "account", [account,])

		if accountResults == 0:
			accountId = self.insertQuery(cursor, self.fa, "(account)", [account,], "RETURNING account_id")
		else:
			accountId = self.selectQuery(cursor, self.fa, "account", [account,], "account_id")

		incomeAdd = [source, income, category, accountId, date]
		incomeColumns = "(source, income, income_category, account_id, dt)"
		incomeId = self.insertQuery(cursor, self.mi, incomeColumns, incomeAdd, "RETURNING income_id")

		# query account balance to be updated
		balance = self.convertDollars(self.selectQuery(cursor, self.fa, "account_id", [accountId,], "balance"))

		# subtract cost from balance and insert into finance history table
		newBalance = balance + income
		historyColumns = "(account_id, balance, dt, income_id)"
		historyValues = [accountId, newBalance, date, incomeId]
		self.insertQuery(cursor, self.fah, historyColumns, historyValues)
		self.updateQuery(cursor, self.fa, "balance", "account_id", [newBalance, accountId])

		self.closeConnection(cursor, connection)

	def transferUpdate(self, source, money, account, details, date):
		cursor, connection = self.createConnection()

		# cursor, table, search, arguments, columns = "*"
		# f"SELECT {columns} FROM {table} WHERE {search} = %s"
		
		# select account id from receive and remove account
		receiveId = self.selectQuery(cursor, self.fa, "account", [source,], "account_id")
		removeId = self.selectQuery(cursor, self.fa, "account", [account,], "account_id")

		# select amount from source account
		receiveBalance = self.convertDollars(self.selectQuery(cursor, self.fa, "account", [source,], "balance"))

		# select amount from account money is being removed from
		removeBalance = self.convertDollars(self.selectQuery(cursor, self.fa, "account", [account,], "balance"))

		# update source account with difference of balance and money
		receiveBalance += money
		self.updateQuery(cursor, self.fa, "balance", "account", [receiveBalance, source])

		# update remove account
		removeBalance -= money
		self.updateQuery(cursor, self.fa, "balance", "account", [removeBalance, account])

		# insert new value into transfers table
		transferColumns = "(amount, from_id, to_id, details, dt)"
		transferValues = [money, removeId, receiveId, details, date]
		transferId = self.insertQuery(cursor, self.transfers, transferColumns, transferValues, "RETURNING id")

		# update balance in account w/ removed balance
		historyColumns = "(account_id, balance, dt, transfer_id)"
		historyValues = [removeId, removeBalance, date, transferId]
		self.insertQuery(cursor, self.fah, historyColumns, historyValues)

		# update balance in account that received money
		historyValues = [receiveId, receiveBalance, date, transferId]
		self.insertQuery(cursor, self.fah, historyColumns, historyValues)

		self.closeConnection(cursor, connection)

	def deleteExpense(self, id):
		cursor, connection = self.createConnection()

		# select account id and type
		accountId = self.selectQuery(cursor, self.me, "expense_id", id, "account_id")
		accountType = self.selectQuery(cursor, self.fa, "account_id", accountId, "account_type")

		# select cost of amount to be deleted from table
		cost = self.convertDollars(self.selectQuery(cursor, self.me, "expense_id", id, "cost"))
		# select balance to update
		balance = self.convertDollars(self.selectQuery(cursor, self.fa, "account_id", accountId, "balance"))

		# depending on account type subtract or add from balance
		if accountType == "credit":
			balance += cost
		else:
			balance -= cost

		# update balance in account table
		self.updateQuery(cursor, self.fa, "balance", "account_id", [balance, accountId])

		# delete from expense and account history tables
		self.deleteQuery(cursor, self.fah, "expense_id", [id,])
		self.deleteQuery(cursor, self.me, "expense_id", [id,])

		self.closeConnection(cursor, connection)