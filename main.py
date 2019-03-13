from timetracker import TimeTracker
import os
import sys

"""
	Main.py
	TimeTracker Driver

	Takes in command line arguments and uses the time tracker class to store information
	
	start initializes the timer

	end
	ends the timer and updates the current day to reflect hour changes and log messages
	needs a message


"""

# db = DB('timetracker.db')

# db.createTable('session', 'key text PRIMARY KEY, value text')
# db.createTable('days', 'date DATE PRIMARY KEY, hours int, message TEXT')




### Main driver code

tracker = TimeTracker()

if len(sys.argv) >= 2: 


	command = sys.argv[1]

	if( command.lower() == '-h'):
		print('Commands')
		print('\t start: Initiate a tracking session')
		print('\t end: Finish a tracking session and store the time spent')
		print('\t add: Adds time and a message to a current days set. ')
		print('\t invoice: Get the time spent within a month and all of its logs.')
		print('\t cancel: Stop the session without saving information')


	if command.lower() == 'start':
		tracker.start()

	if command.lower() == 'end':
		if(len(sys.argv) < 3):
			print("A message is needed for the log.")
		else:
			tracker.end(sys.argv[2])

	if command.lower() == 'cancel':
		tracker.cancel()

	if command.lower() == 'status':
		tracker.status()


	if command.lower() == 'invoice':
		if len(sys.argv) < 4: 
			print("Invoice requires a month and year")
		else:
			tracker.invoice(int(sys.argv[2]), int(sys.argv[3]))

else:
	print("Time tracking requires arguements. Try -h to see commands.")
