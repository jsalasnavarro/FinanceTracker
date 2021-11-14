from datetime import datetime
from finance import Finance
import ezsheets
import csv

class ImportFile:
	def __init__(self, fileName, tableName):
		# file fileName
		self.fileName = fileName
		self.tableName = tableName

	def csvFile(self):
		# open csv
		with open(self.fileName, newline = '') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			# skip header
			next(reader)

			# loop through rows
			for row in reader:
				newRow = []
				# loop through column values in row
				for ndx,col in enumerate(row):
					value = self.checkValues(col,ndx,'csv')
					newRow.append(value)
				newExpense = Finance(self.tableName, newRow[0], newRow[1], newRow[2], newRow[3], 
									 newRow[4]).setExpense()

		return 'csv done uploading!'

	def googleSheets(self):
		# access spreadsheet object
		ss = ezsheets.Spreadsheet(self.fileName)

		# access sheets in spreadsheet object
		sheets = ss.sheets
		
		category = []
		for title in ss.sheetTitles:
			for row in range(ss[title].rowCount):
				newRow = []
				for col in range(ss[title].columnCount):
					value = ss[title][col + 1, row + 1]
					# check for blank cells in sheet
					if value != "" and value != None:
						# skip header
						if row  == 0:
							continue
						# check all other values
						else:
							value = self.checkValues(value,col,'googleSheet')

						newRow.append(value)

				# skip any blank rows from sheet and header
				if newRow != [] and row != 0:
					finalRow = checkValues(newRow[0], newRow[1], newRow[2], newRow[3], newRow[4])
					# instantiate expense class and call method to insert row of sheet values
					newExpense = Finance(self.fileName, newRow[0], newRow[1], newRow[2], newRow[3], 
										 newRow[4]).setExpense()
		return ' google sheet done uploading!'

		def checkValues(self, value, index,file):
			# source
			if index == 0:
				value = value.lower()
				
			# money
			# test if value can be converted to a float
			elif index == 1:
				try:
					testValue = value.replace('$','')
					testValue = testValue.replace(' ', '')
					testValue = testValue.replace(',', '')
					value = float(testValue)
				except:
					value = 00.00

			# category
			elif index == 2:
				try:
					value = value.lower()
				except:
					value = 'ERROR'
				# if row[2] not in category:
				# 	category.append(value)

			# account
			elif index == 3:
				try:
					value = value.lower()
				except:
					value = 'ERROR'
				# check if value exists in database
				# if row[3] not in paymentTypes:
				# 	paymentTypes.append(value)

			# date
			# will have two different date formats for database and display
			elif index == 4 and file == 'googleSheet':
				try:
					parse = datetime.strptime(value, '%A, %B %d, %Y')
				
				except:
					parse = datetime.strptime('Monday, January 1, 1900', '%A, %B %d, %Y')
				# format datetime type to string w/format for query
				value = datetime.strftime(parse, '%Y-%m-%d')

			elif index == 5 and file == 'csv':
				try:
					value = datetime.strftime(value, '%Y-%m-%d')
				except:
					value = '1990-01-01'

			return value