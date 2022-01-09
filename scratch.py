from finance import Finance
from importfile import ImportFile
import csv
import sys
import psycopg2
from datetime import datetime

import numpy as np
import pandas as pd
from sqlalchemy import create_engine


# newCsv = ImportFile('monthly_expenses.csv', 'monthly_expenses_test').csvFile()
# print(newCsv)
finance = Finance()

# source, money, category, account, date, details(if any)
# newExpense = finance.setExpense()

# add income individually
# source, money, category, account, date
# newIncome = finance.setIncome()

# transfer funds
# source, money, account, date, details = ""
# newTransfer = finance.transferFunds()
	
# delete an expense using expense id
# finance.deleteValue()

# dataQuery = "select fa.account, ah.balance, me.cost, me.vendor, ec.expense_category, me.details, me.dt \n\
# 			from monthly_expenses me \n\
# 			join expense_categories ec on ec.category_id = me.category_id \n\
# 			join finance_account_history ah on ah.expense_id = me.expense_id \n\
# 			join finance_accounts fa on fa.account_id = me.account_id \n\
# 			order by me.expense_id desc"

# engine = create_engine("postgresql+psycopg2://@localhost/finances")
# data = pd.read_sql_query(dataQuery, engine)
