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
		numSheets = len(ezsheets.listSpreadsheets())
		
		for sheet in range(numSheets):
			for row in range(sheets[sheet].rowCount):
				newRow = []
				for col in range(sheets[0].columnCount):
					value = sheets[0][col + 1, row + 1]
					# check for blank cells in sheet
					if value != "":
						# skip header
						if row  != 0:
							# date column
							if (col == 4):
								# parse string to a datetime, format datetime type to string w/ 
								# format for query
								value = datetime.strftime(datetime.strptime(value, '%A, %B %d, %Y'), '%Y-%m-%d')
						
						newRow.append(value)

				# skip any blank rows from sheet and header
				if newRow != [] and row != 0:
					# instantiate expense class and call method to insert row of sheet values
					newExpense = Expense(newRow[0], newRow[1], newRow[2], newRow[3], newRow[4]).setExpense()
		return 'Done!'