from finance import Finance
from importfile import ImportFile
import csv
import sys
import psycopg2

# newCsv = ImportFile('monthly_expenses.csv', 'monthly_expenses_test').csvFile()
# print(newCsv)

# vendor, cost, category, account, date, details (if any)
newExpense = Finance().setExpense()

# add income individually
# source, money, category, account, date
# newIncome = Finance().setIncome()

# transfer funds
# source, money, category, account, date, details = ""
# newTransfer = Finance().transferFunds()
	