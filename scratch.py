from expense import Expense
from importfile import ImportFile
import ezsheets
from datetime import datetime

# import file data from google spreadsheets file
# newFile = ImportFile("Copy of Finances").googleSheets()
# print(newFile)

# add expenses indidividually
# vendor, cost, category, paymentType, date
newExpense = Expense('Harmons', '$56.12','groceries', 'afcc', '2021-11-03').setExpense()
newExpense = Expense('car repairs-fuel pressure regulator', '$61.41','autozone', 'afcc', '2021-11-03').setExpense()
newExpense = Expense('Petco', '$7.53','Clifford-treats', 'afcc', '2021-11-03').setExpense()
newExpense = Expense('ProRenter', '$1528','rent', 'citi', '2021-11-01').setExpense()
newExpense = Expense('northface', '$59.27','remainder', 'citi', '2021-11-01').setExpense()
newExpense = Expense('comcast', '$50.80','wifi', 'citi', '2021-11-01').setExpense()


# # access spreadsheet object
# ss = ezsheets.Spreadsheet('Copy of Finances')

# # access sheets in spreadsheet object
# sheets = ss.sheets

# for title in ss.sheetTitles:
# 	print(title)
# access spreadsheet object
# ss = ezsheets.Spreadsheet("Copy of Finances")

# # access sheets in spreadsheet object
# sheets = ss.sheets

# # run query for stored categories, table to be added
# paymentTypes = ['afcc', 'discover', 'citi', 'paypal', 'cash']

# for title in ss.sheetTitles:
# 	for row in range(ss[title].rowCount):
# 		newRow = []
# 		for col in range(ss[title].columnCount):
# 			value = ss[title][col + 1, row + 1]
# 			# check for blank cells in sheet
# 			if value != "" or not None:
# 				# skip header
# 				if row  != 0:
# 					# vendor
# 					if col == 0:
# 						print(col, type(value))
# 					# cost
# 					if col == 1:
# 						# test if value can be converted to a float
# 						try:
# 							testValue = value.replace('$','')
# 							testValue = testValue.replace(' ', '')
# 							testValue = testValue.replace(',', '')
# 							testValue = float(testValue)
# 						except:
# 							value = 00.00
# 					# category
# 					if col == 2:
# 						value = value.lower()
# 						if value not in paymentTypes:
# 							paymentTypes.append(value)

# 					# payment type
# 					if col == 3:
# 						# check if payment type is new
# 						print(col, type(value))
# 					# date
# 					if col == 4:
# 						print(col, type(value))
# 						# parse string to a datetime
# 						try:
# 							parse = datetime.strptime(value, '%A, %B %d, %Y')
						
# 						except:
# 							parse = datetime.strptime('0000-00-00', '%A, %B %d, %Y')

# 						# format datetime type to string w/format for query
# 						value = datetime.strftime(parse, '%Y-%m-%d')