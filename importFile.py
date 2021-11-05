from datetime import datetime
from expense import Expense
import ezsheets

class ImportFile:
	def __init__(self, name):
		# name of google spread sheet name
		self.name = name

	def googleSheets(self):
		# access spreadsheet object
		ss = ezsheets.Spreadsheet(self.name)

		# access sheets in spreadsheet object
		sheets = ss.sheets

		# run query for stored categories, table to be added
		paymentTypes = ['afcc', 'discover', 'citi', 'paypal', 'cash']
		category = []
		for title in ss.sheetTitles:
			for row in range(ss[title].rowCount):
				newRow = []
				for col in range(ss[title].columnCount):
					value = ss[title][col + 1, row + 1]
					# check for blank cells in sheet
					if value != "" and value != None:
						# skip header
						if row  != 0:

							# # vendor
							if col == 0:
								value = value.lower()
								
							# cost
							if col == 1:
								# test if value can be converted to a float
								try:
									testValue = value.replace('$','')
									testValue = testValue.replace(' ', '')
									testValue = testValue.replace(',', '')
									testValue = float(testValue)
								except:
									value = 00.00
							# category
							if col == 2:
								value = value.lower()
								if value not in category:
									category.append(value)

							# payment type
							if col == 3:
								value = value.lower()
								if value not in paymentTypes:
									paymentTypes.append(value)

							# date
							if col == 4:
								# parse string to a datetime
								try:
									parse = datetime.strptime(value, '%A, %B %d, %Y')
								
								except:
									parse = datetime.strptime('Monday, January 1, 1900', '%A, %B %d, %Y')
								# format datetime type to string w/format for query
								value = datetime.strftime(parse, '%Y-%m-%d')
						
						newRow.append(value)

				# skip any blank rows from sheet and header
				if newRow != [] and row != 0:
					# instantiate expense class and call method to insert row of sheet values
					newExpense = Expense(newRow[0], newRow[1], newRow[2], newRow[3], newRow[4]).setExpense()
		return 'Done!'