from finance import Finance
from importfile import ImportFile
import csv
import sys
import psycopg2
from datetime import datetime

# newCsv = ImportFile('monthly_expenses.csv', 'monthly_expenses_test').csvFile()
# print(newCsv)
finance = Finance()

# source, money, category, account, date, details(if any)
# newExpense = Finance().setExpense()

# add income individually
# source, money, category, account, date
# newIncome = Finance().setIncome()

# transfer funds
# source, money, category, account, date, details = ""
# newTransfer = Finance().transferFunds()
	
# delete an expense
# finance.deleteValue()



# connection = psycopg2.connect(dbname = "finances", host = "localhost")
# cursor = connection.cursor()

# query = "select * from monthly_expenses"
# cursor.execute(query)
# results = cursor.fetchall()
# print(type(res))