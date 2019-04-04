#!/usr/bin/python3
# &													BOTS MEMORY											
#---------------------------------------------------------------------------------------------------------------------------------------#

import os
from os.path import expanduser
from todoBot import bot_types
from todoBot.timeManip import caclTime, now, todayIn, tomorrowIn, secToTime, dSecToTime

#---------------------------------------------------------------------------------------------------------------------------------------#

def findPattern(pattern):
	pat1 = pattern.find('%i')
	pat2 = pattern.find('%c')
	pat3 = pattern.find('%s')

	res = min(pat1, pat2)
	if res == -1:
		res = max(pat1, pat2)
	
	temp = min(pat3, res)			
	if temp == -1:
		res = max(pat3, res)
	else:
		res = temp
	
	return res

def patternTrans(lst, pattern, ret = []):
	if lst == []:
		return ret

	ind = findPattern(pattern)
	answ = pattern[ind + 1 : ind + 2]
	
	if answ == 'i':
		res = int(lst[0])
	elif answ == 's':
		res = str(lst[0])
	elif answ == 'c':
		res = chr(lst[0])
	else:
		return -1 
	
	ret.append(res)
	return patternTrans(lst[ 1 : len(lst)], pattern[ ind + 2: len(pattern)], ret = ret)

def toType(lst, pattern):
	return patternTrans(lst, pattern, ret = [])

class dbLite():
	def __init__(self, name):
		self.name = name
		self.bord = " %i"

	def init(self, bord = ''):
		if bord != '':
			self.bord = bord
		
		self.table = self.getdb()

	def getdb(self):
		try:
			file = open(self.name, "r")
		except FileNotFoundError:
			t = open(self.name, "w+")
			t.close()
			return []
			
		text = file.readlines()
		file.close()
	
		ret = list()
		for temp in text:
			words = temp.split(self.bord[0])
			res = toType(words[1 : len(words)], self.bord)
			try:
				ret.append([int(words[0]), res[0]])
			except ValueError:
				return []

		return ret

	def commit(self, table = []):
		if table == []:
			table = self.table

		file = open(self.name, "w")

		for item in table:
			fl = "%i"+ self.bord + "\n"
			file.write(fl % (item[0], item[1]) )

		file.close()
		return table

	def add(self, id, value):
		if(self.get(id) != []):
			return 1

		self.table.append([int(id), int(value)])	
		self.commit()
		return 0

	def delete(self, id):
		res = list()
		for item in self.table:
			if(item[0] != id):
				res.append(item)
		
		self.table = res
		return self.commit()

	def get(self, id):
		for item in self.table:
			if(item[0] == id):
				return item
		return []

	def change(self, id, newValue):
		self.delete(id)
		self.table.append([int(id), newValue])	
		return self.commit()

	def show(self):
		print("#-------------------------------#")
		
		for x in self.table:
			print(x)

		print("#-------------------------------#")
		return self.table

	def drop(self):
		return os.remove(self.name)

	def getTable(self):
		return self.table

	def getName(self):
		return self.name

#---------------------------------------------------------------------------------------------------------------------------------------#

class dbStandart():
	def __init__(self, name):
		self.name = name
		self.bord = " %i %i %i %i"

	def init(self, bord = ''):
		if bord != '':
			self.bord = bord

		self.table = self.getdb()

	def getdb(self):
		try: 
			file = open(self.name, "r")
		except FileNotFoundError:
			t = open(self.name, "w+")
			t.close()
			return []

		text = file.readlines()
		file.close()
		
		ret = list()
		for temp in text:
			words = temp.split(self.bord[0])
			res = toType(words[1 : len(words)], self.bord)
			try:
				ret.append([int(words[0]), res[0], res[1], res[2], res[3]])
			except ValueError:
				return []

		return ret

	def commit(self, table = ""):
		if table == "":
			table = self.table

		file = open(self.name, "w")
		fl = "%i"+ self.bord + "\n"

		for item in table:	
			file.write(fl % (item[0], item[1], item[2], item[3], item[4]))

		file.close()
		self.table = table
		return table
	
	def cAdd(self, id, name, field0, field1, field2):
		self.table.append([int(id), name, field0, field1, field2])
		return 0

	def add(self, id, name, field0, field1, field2):
		self.table.append([int(id), name, field0, field1, field2])
		self.commit()
		return 0

	def delB(self, field, value):
		res = list()

		for item in self.table:
			if(item[field] != value):
				res.append(item)

		return self.commit(res)

	def delD(self, field0, value0, field1, value1):
		res = list()

		for item in self.table:
			if item[field0] != value0 or item[field1] != value1: 
				res.append(item)

		return self.commit(res)

	def getB(self, field, value):
		ret = list()

		for item in self.table:
			if(item[field] == value):
				ret.append(item)

		return ret

	def getD(self, field0, value0, field1, value1):
		ret = list()

		for item in self.table:
			if(item[field0] == value0 and item[field1] == value1):
				ret.append(item)

		return ret


	def set(self, lst):	
		self.table = lst

	def linesOfB(self, search, field, value):
		ret = list()

		for item in self.table:
			if(item[field] == value):
				ret.append(item[search])

		return ret

	def linesOfD(self, search, field0, value0, field1, value1):
		ret = list()

		for item in self.table:
			if(item[field0] == value0 and item[field1] == value1):
				ret.append(item[search])

		return ret

	def show(self):
		print("#-------------------------------#")
		
		for x in self.table:
			print(x)

		print("#-------------------------------#")
		return self.table
		
	def dropTable(self):
		os.remove(self.name)

	def getTable(self):
		return self.table

	def getName(self):
		return self.name

#---------------------------------------------------------------------------------------------------------------------------------------#

class Database:
	def __init__(self):
		self.dbTable = expanduser("~") + "/.rbBot/database.db"
		self.dbReal = expanduser("~") + "/.rbBot/toDoList.db"
		self.dbTemp = expanduser("~") + "/.rbBot/temp.db"
		self.table = dbStandart(self.dbTable)
		self.realTable = dbStandart(self.dbReal) 
		self.tempTable = dbLite(self.dbTemp)
		self.table.init(bord = "&%s&%s&%i&%i")
		self.realTable.init(bord = "&%s&%s&%i&%i")
		self.tempTable.init()
#														REAL TABLE
#---------------------------------------------------------------------------------------------------------------------------------------#
	
	def updateRealTable(self):
		self.realTable.init("&%s&%s&%i&%i")

	def commitReal(self, table = []):
		if table == []:
			table = self.realTable.getTable()

		return self.realTable.commit(table = self.db_sort(table))

	def addRealItem(self, userID, task, desc, tType, time):
		if tType == -1:				
			return 1

		self.delRealD("userID", userID, "task", task)
		
		if time == -1:
			print("non time")
			Time = 0 
			targTime = 972532281307			
		elif tType == bot_types.FIXED:
			print("Fixed time")
			Time = int(time)
			targTime = todayIn(Time)
			
			if (now() + 30) > targTime:
				print("Tomorrow")
				targTime = tomorrowIn(Time)
			else:
				print("Today")
		else: 
			print("floating time")
			targTime = now() + int(time) 
			Time = bot_types.REAL_FLOATING

		print(now(), targTime, Time)
		
		self.realTable.cAdd(userID, task, desc, int(Time), int(targTime) )
		return self.commitReal()
	
	def delRealD(self, field0, value0, field1, value1):
		field0 = self.fieldToIndex(field0)
		field1 = self.fieldToIndex(field1)
		return self.realTable.delD(field0, value0, field1, value1)
	
	def delRealB(self, field, value):
		field = self.fieldToIndex(field)
		return self.realTable.delB(field, value)
	
	def getRealD(self, field0, value0, field1, value1):
		return self.realTable.getD(self.fieldToIndex(field0), value0, self.fieldToIndex(field1), value1)

	def showRealTable(self):
		table = self.realTable.getTable()
		print("#-------------------------------#")
		
		for x in table:
			print(x, dSecToTime( x[4] ))

		print("#-------------------------------#")
		return table

	def dropRealTable(self):
		return self.realTable.dropTable()

#---------------------------------#
#---------------------------------#
#---------------------------------#
#---------------------------------#

	def getRealTime(self, userID, task):
		for item in self.realTable.getTable():
			if item[0] == userID and item[1] == task:
				return item[4]
		return []

#														STATUS (TEMP) TABLE
#---------------------------------------------------------------------------------------------------------------------------------------#

	def commitTemp(self):
		return self.tempTable.commit()

	def addStatus(self, userID, status):
		return self.tempTable.add(userID, status)

	def delStatus(self, userID):
		return self.tempTable.delete(int(userID))

	def getStatus(self, userID):
		return self.tempTable.get(userID)

	def changeStatus(self, userID, newValue):
		return self.tempTable.change(userID, newValue)

	def showTemp(self):
		return self.tempTable.show()

	def dropTemp(self):
		return self.tempTable.dropTable()
#														MAIN TABLE														
#---------------------------------------------------------------------------------------------------------------------------------------#
	
	def commit(self, table = []):
		if table == []:
			table = self.table.getTable()
				 
		table = self.db_sort(table)
		return self.table.commit(table = table)
		
	def delB(self, field, value):
		field = self.fieldToIndex(field) 
		print(field)
		self.delRealB(field, value)
		return self.table.delB(field, value)

	def delD(self, field0, value0, field1, value1):
		field0 = self.fieldToIndex(field0)
		field1 = self.fieldToIndex(field1)
		
		self.delRealD(field0, value0, field1, value1)
		return self.table.delD(field0, value0, field1, value1)

	def getB(self, field, value):
		return self.table.getB(self.fieldToIndex(field), value)

	def getD(self, field0, value0, field1, value1):
		return self.table.getD(self.fieldToIndex(field0), value0, self.fieldToIndex(field1), value1)

	def showTable(self):
		return self.table.show()
		
	def dropTable(self):
		return self.table.dropTable()

#---------------------------------#
#---------------------------------#
#---------------------------------#
#---------------------------------#

	def linesOfB(self, search, field, value):
		return self.table.linesOfB(self.fieldToIndex(search),  self.fieldToIndex(field), value) 
		
	def linesOfD(self, search, field0, value0, field1, value1):
		return self.table.linesOfD( 
		self.fieldToIndex(search),
		self.fieldToIndex(field0), value0,
		self.fieldToIndex(field1), value1)

	def getUserTasks(self, id):
		return self.table.linesOfB(1 ,0, id)	

	def cAdd(self, userID, task, desc, tType, time):
		userID = int(userID)
		task = str(task)
		desc = str(desc)
		tType = int(tType)
		time = int(time)

		if(self.table.getD(0, userID, 1, task) != []):
			return 1

		self.table.cAdd(userID, task, desc, tType, time)

		self.commit()
		return 0

	def add(self, userID, task, desc, tType, time):
		if self.cAdd(userID, task, desc, tType, time) == 1:
			return 1
			 
		if(tType == bot_types.FIXED):
			self.addRealItem(userID, task, desc, tType, time)

		return 0
		
	def changeField(self, userID, task, field, newValue):
		temp = self.getD("userID", userID, "task", task)
		if temp == []:
			return 1

		temp = temp[0]
		
		self.delD("userID", temp[0], "task", temp[1])

		if(field == "task"):
			return self.add(temp[0], str( newValue ),   temp[2], temp[3], temp[4])
		elif(field == "desc" ):
			return self.add(temp[0], temp[1], str( newValue ),   temp[3], temp[4])
		elif(field == "type" ):
			return self.add(temp[0], temp[1], temp[2], int( newValue ),   temp[4])
		elif(field == "time"):
			return self.add(temp[0], temp[1], temp[2], temp[3], int(newValue ) )
		else:
			print("Wrong argument!")
			return 1

	def delU(self, userID):
		res = list()
		realRes = list()

		table = self.table.getTable()
		for item in table:
			if item[0] != userID or item[4] >= 0: 
				res.append(item)
		table = res

		realTable = self.realTable.getTable()
		for item in realTable:
			if item[0] != userID or item[4] >= 0 and item[4] != 972532281307: 
				realRes.append(item)
		
		realTable = realRes

		self.realTable.set(realRes) 
		self.table.set(res)
		
		self.commit()
		self.commitReal()

	def getUncomp(self, userID):
		for x in self.table.getTable():
			if x[0] == userID and x[4] == -1:
				return x 
		return []

	def start(self, userID):
		for x in self.table.getTable(): 
			if x[0] == userID and x[3] == bot_types.FLOATING:
				self.addRealItem(int(x[0]), x[1], x[2], int(x[3]), int(x[4]))

	def startOne(self, userID, task):
		x = self.getD("userID", userID, "task", task)[0]
		
		rl = self.getRealD("userID", userID, "task", task) 
		print(rl)
		if rl != []:
			if rl[0][3] == -1:
				self.delRealD("userID", userID, "task", task)

		targTime = now() + x[4] 
		print("started",x[0],x[1], now(), targTime)
		
		self.realTable.cAdd(userID, task, x[2], int(bot_types.REAL_FLOATING), targTime )
		return self.commitReal()

#														OTHER STUFF
#---------------------------------------------------------------------------------------------------------------------------------------#
	
	def addAllTasks(self):
		for x in self.table.getTable(): 
			if x[3] != 1:
				self.addRealItem(x[0], x[1], x[2], x[3], x[4])		

	def db_sort(self, table):
		res = table
		for i in range(len(res)):
			for j in range(len(res) - 1):
				if res[i][4] < res[j][4]:
					temp = res[i]
					res[i] = res[j]
					res[j] = temp
		return res

	def notInList(self, search, target):
		for item in target:
			if search[0] == item[0] and search[1] == item[1]:
				return 0
		return 1

	def fieldToIndex(self, field):
		if(field == "userID"):
			return 0
		elif(field == "task"):
			return 1
		elif(field == "desc"):
			return 2
		elif(field == "type"):
			return 3
		elif(field == "time"):
			return 4
		else:
			return field

if __name__ == "__main__":
	db = Database()