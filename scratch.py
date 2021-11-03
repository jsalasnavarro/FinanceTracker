from expense import Expense
from importfile import ImportFile

# expense, cost, details, payment, date, password)
# expenses = [['test2', '100.00', 'rent', 'discover', '2021-10-31'], ['test3', '56.40', 'groceries', 'citi', None]]		

# newExpense = Expense('test1', 105.50, 'fun money', 'citi', '2021-10-11','northernlights')
# newExpense.setExpense()

# for exp in expenses:
# 	newExpense = Expense(exp[0], exp[1], exp[2], exp[3], exp[4])
# 	newExpense.setExpense()

newFile = ImportFile("Copy of Finances").googleSheets()
print(newFile)