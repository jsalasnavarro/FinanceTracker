from finance import Finance
from importfile import ImportFile
import csv
import sys
import psycopg2

# newCsv = ImportFile('monthly_expenses.csv', 'monthly_expenses_test').csvFile()
# print(newCsv)


# add expenses indidividually
# source, cost, category, account, details(if any), date
# newExpense = Finance().setExpense()

# add income individually
# source, money, category, account, date
# newIncome = Finance().setIncome()


# connection = psycopg2.connect(dbname='finances', host='localhost')
# cursor = connection.cursor()

# check = ['christmas gifts',]
# query = "select category_id from expense_categories where expense_category = %s"
# cursor.execute(query, check)

# results = cursor.fetchall()
# connection.commit()
# cursor.close()
# connection.close()

# print(len(results))
	