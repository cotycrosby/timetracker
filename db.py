import sqlite3

###
#
#	Class DB
#	database handler class. 
# 	Creates tables, handles insertions deletions and selects
#	Honestly I think that the update, insert, and query functions might be a little bit extra. Who knows.
#
###
class DB():



	def __init__(self, database = None):

		if database == None:
			print('Need a database')
			return
		
		self.conn = sqlite3.connect(database) 
		self.c = self.conn.cursor()

	def __del__(self):
		self.conn.close()


	###
	#	Creates a table only if it doesn't exists
	#	Takes two strings: tableName and columns
	#	return: void
	###
	def createTable(self, tableName, columns):
		self.c.execute("CREATE TABLE IF NOT EXISTS " + tableName + " ( " + columns + " )")
		self.conn.commit()

	###
	#	Inserts or updates a field
	#	Takes two strings:  tableName, columnString
	#	return: void
	###
	def insert(self, tableName, columns, values ):
		self.c.execute("INSERT  INTO " + tableName + " ( " + columns + " ) VALUES ( " + values + ");")
		self.conn.commit()

	###
	#	Updates an existing field
	# 	Takes the table, the assignment string, and the where clause
	# 	eg update('session', "key = 'time', value = '123' ", "key = 'startTime' ")
	def update(self, tableName, setQuery, whereClause):
		self.c.execute("UPDATE " + tableName + " SET " + setQuery + " WHERE " + whereClause )
		self.conn.commit()

	def delete( self, tableName, whereClause):
		self.c.execute("DELETE FROM " + tableName + " WHERE " + whereClause )
		self.conn.commit()


	###
	#	find - findMany
	#	takes the table and whereclause string
	#	returns a single list or a list of lists
	###
	def find(self, tableName, whereClause = '1 = 1'):
		res = self.c.execute("SELECT * FROM " + tableName + " WHERE " + whereClause)
		return res.fetchone()

	def findMany(self, tableName, whereClause = '1 = 1'):
		res = self.c.execute("SELECT * FROM " + tableName + " WHERE " + whereClause )
		return res.fetchall()

	###
	#	Query
	#	Used for doing more cuintostom querys.
	#	returns void
	###
	def query(self, query):
		res = self.c.execute(query)
		self.conn.commit()
		return res

		
