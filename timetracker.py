import sqlite3
from datetime import datetime
from calendar import monthrange
from db import DB


class TimeTracker:
	__DB__NAME = 'timetracker.db'
	__SESSION_TABLE = 'session'
	__DAYS_TABLE = 'days'

	# constructor
	def __init__(self):
		# ensure that the database is connected and tables created
		self.db = DB(self.__DB__NAME)

		self.db.createTable('days', 'date DATE PRIMARY KEY, hours REAL, message TEXT')
		self.db.createTable('session', 'key TEXT PRIMARY KEY, value TEXT')


		self.currentDate = datetime.now().date()


	#### main methods ####
	def start(self):
		
		if self.sessionStart():
			print("Starting tracker...")
		else:
			print("Tracker already initiated.")




	def end(self, message):
		timeSpent = self.getTimeSpent();

		if timeSpent == None: 
			print("Timer not initiated.")
			return None

		

		#convert to number of float numHours
		timeSpent = round(timeSpent.total_seconds()/60/60, 2)

		# round up to next quarter hour - ie: .45 hours to .5 hours (25 minutes to 30 minutes)
		timeSpent = timeSpent - (timeSpent % .25 ) + .25

		self.updateDate(timeSpent, message)

		# delete the session record
		self.sessionEnd()

	def add(self, time, message):
		self.updateDate(time, message)
		


	### Displays all records for a given month and year
	def invoice(self, month, year):

		_, numDays = monthrange(year, month)



		## format the year and month 
		year = str(year)
		if month < 10:
			month = '0' + str(month)
		else:
			month = str(month)

		start = year + '-' + month + '-01';
		end = year + '-' + month + '-' + str(numDays);


		whereClause = "date between '" + start + "' and '" + end + "'"

		
		recordedDays = self.db.findMany('days', whereClause)

		totalHours = 0
		for day in recordedDays:
			day, hours, message = day[0], day[1], day[2]

			totalHours += hours

			# message = message.split(':').join()
			message = '\n\t'.join(message.split(':'))

			print(str(day) + ' - ' + str(hours) + 'h')
			print('\t' + message)

		print("\nTotal Hours: " + str(totalHours))
		

	## end the session without updating the days table.
	def cancel(self):
		if self.getSessionTime() == None:
			print("No active session.")
		else:
			self.sessionEnd()
			print("Session cancelled")

	def status(self):
		startTime = self.getSessionTime()

		if startTime == None:
			print('No active session.')
			return None


		print('Active session in progress: ' + str(self.getTimeSpent()) )




	#### Helper functions ####

	def findCurrentDateInDb(self):
		return self.db.find('days', "date = '" + str(self.currentDate) + "'")

	def insertDate(self, hours, message):
		valueString = " '{}', {}, '{}'".format(str(self.currentDate), hours, message)
		self.db.insert('days', 'date, hours, message', valueString )

	def updateDate(self, hours, message):
		day = self.findCurrentDateInDb()

		if( day == None ):
			self.insertDate(hours, message)
			print('Date information created.')
			return;

		day = day[0]

		setString = "hours = hours + " + str(hours) + ", message = message || ':" + message + "'"
		whereClause = "date = '" + day + "'"
		## update the data
		self.db.update('days', setString, whereClause )







	# saves the starting time in a "session variable" called startTime
	# returns bool.
	def sessionStart(self):
		if self.db.find('session', "key = 'startTime'") != None:
			return False

		self.db.insert('session', 'key, value', "'startTime', DATETIME('now','localtime')")
		return True

	# returns the difference between the current time and the startTime
	def getTimeSpent(self):
		startTime = self.getSessionTime()

		if startTime == None:
			return None


		# return the difference
		return datetime.now() - datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")

	def getSessionTime(self):
		# get the stored start time
		startTime = self.db.find('session', "key = 'startTime'")
		if startTime == None:
			return None

		return startTime[1]
		
	
	# Deletes the session startTime record
	def sessionEnd(self):
		return self.db.delete('session', "key = 'startTime'")

