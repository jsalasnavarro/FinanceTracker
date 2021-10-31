import ezsheets
from datetime import datetime

# name of spreadsheet 
sheet = "Copy of Finances"

# access spreadsheet object
ss = ezsheets.Spreadsheet(sheet)

# access sheets in spreadsheet object
sheets = ss.sheets

# for s in sheets:
# 	# print(s.title, s.sheetId, s.rowCount, s.columnCount)
# 	for row in s.rowCount:
data = []
for row in range(sheets[0].rowCount):
	newRow = []
	for col in range(sheets[0].columnCount):
		value = sheets[0][col + 1, row + 1]
		# check for blank cells in sheet
		if value != "":
			# look for date column to format values for query
			if row  != 0:
				# date column
				if (col == 4):
					# parse string to a datetime, format datetime type to string w/ 
					# format for query
					value = datetime.strftime(datetime.strptime(value, '%A, %B %d, %Y'), '%Y-%m-%d')
			
			newRow.append(value)
	# skip any blank rows from sheet and header
	if newRow != [] and row != 0:
		data.append(newRow)
print(data)