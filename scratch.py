from expense import Expense
# expense, cost, details, payment, date, password)
pword = 'northernlights'
expenses = [['test', '100.00', 'rent', 'discover', '2021-11-01'], ['test1', '56.40', 'groceries', 'citi', '2021-11-02']]

# newExpense = Expense('test1', 105.50, 'fun money', 'citi', '2021-10-11','northernlights')
# newExpense.setExpense()

for exp in expenses:
	newExpense = Expense(exp[0], exp[1], exp[2], exp[3], exp[4], pword)
	newExpense.setExpense()