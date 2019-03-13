# Timetracker

I built this on python version 2.7.15


This program tracks time spent on tasks through the command line.


To run the program type `python path/to/script/main.py start` 
(I recommend creating an alias for this. == tt)

`tt status`
Check your current session. Outputs the time spent

`tt cancel`
Doesn't save the current session in the database

`tt end "Message"`
Stores the time spent with a message.

`tt invoice #month #year`
Gets the total time spent and messages for each date


### How it works?
Main.py acts as a main driver. It interacts with the timetracker class to handle the records. The database handle hands all recording. 

