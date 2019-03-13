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

		day = self.findCurrentDateInDb()

		if( day == None ):
			self.insertDate(timeSpent, message)
			print('Date information created.')
		else:
			day = day[0]
			self.updateDate(day, timeSpent, message)
			print('Date information appended.')

		# delete the session record
		self.sessionEnd()



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

	def updateDate(self, day, hours, message):

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


# class TimeTracker:

# 	__DB_NAME = 'timetracker.db'

# 	### Constructor
# 	def __init__(self):

# 		# initialize the db
# 		self.connection = sqlite3.connect(self.__DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES) 
# 		self.cursor = self.connection.cursor();


# 		# set the current date
# 		self.currentDate = datetime.now().date()

# 		# print(self.findDate())

# 		# self.invoice(3, 2019)
		

	
# 	### Destructor
# 	def __del__(self):
# 		self.connection.close()


# 	### public
# 	# allows the user to change the date for inserts.
# 	def changeDate(dateString):
# 		self.currentDate = dateString


# 	def findDate(self):
# 		self.cursor.execute("SELECT * FROM days WHERE date = ?", (self.currentDate,	));
# 		return self.cursor.fetchone()


# 	### updates a sentinal record in the database to store the starting time to track
# 	def start(self):
# 		now = datetime.now();
# 		self.cursor.execute("UPDATE days SET date = DATETIME('now','localtime') WHERE hours = -1")
# 		self.connection.commit();

# 	def end(self , message = "No message"):
# 		now = datetime.now()
# 		# Get the stored time from the db.
# 		self.cursor.execute("SELECT date FROM days where hours = -1");
# 		startTime = self.cursor.fetchone()[0];
# 		# convert the time from  unicode to datetime
# 		startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
# 		#find the difference
# 		timeDiff = now - startTime

# 		#convert to double
# 		timeDiff = round(timeDiff.total_seconds()/60/60, 2)

# 		# round up to next quarter hour
# 		hoursWorked = timeDiff - (timeDiff % .25 ) + .25


# 		# check to see if I already worked that day.
# 		self.cursor.execute("SELECT * FROM days where date = ?", (self.currentDate, ))

# 		result = self.cursor.fetchone()	

# 		# if I don't have an entry for the day create one	
# 		if result == None:
# 			self.cursor.execute("INSERT INTO days VALUES(?, ? ?)", (self.currentDate, hoursWorked, message))
# 		else:
# 			# otherwise add on the hours and append the message
# 			hoursWorked += result[1]
# 			message = result[2] + ":" + message # message probably shouldn't include a colon.
# 			self.cursor.execute("UPDATE days SET hours = ?, message = ?", (hoursWorked, message))

# 		self.connection.commit()


# 	def invoice(self, month, year):

# 		_, numDays = monthrange(year, month)



# 		## format the year and month 
# 		year = str(year)
# 		if month < 10:
# 			month = '0' + str(month)
# 		else:
# 			month = str(month)

# 		start = year + '-' + month + '-01';
# 		end = year + '-' + month + '-' + str(numDays);

# 		self.cursor.execute("SELECT * FROM days WHERE date between ? and ?", (start, end))
# 		print(self.cursor.fetchall())





# 	def __del__(self):
# 		self.connection.close()
