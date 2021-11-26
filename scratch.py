from finance import Finance
from importfile import ImportFile
import csv
import sys

# newCsv = ImportFile('monthly_expenses.csv', 'monthly_expenses_test').csvFile()
# print(newCsv)


# add expenses indidividually
# vendor, cost, category, paymentType, date
newExpense = Finance('harmons', 45.54, 'groceries', 'afcc', '2021-11-24').setExpense()


# add income individually
# newIncome = Finance().setIncome()