#!/usr/bin/python3
# -*- coding: utf-8 -*-

import todoBot.telebot, config, time
from todoBot import bot_types, bot_variables, types
from todoBot.database import Database, dbLite
from os.path import expanduser
from todoBot.timeManip import toSeconds, secToTime, nStr, getShortTime, getTime, sumTime, subTime, now
from todoBot.timeManip import inCountries, getTzList, getCountryCode, getTzShortTime, inTzCodes, inTz
import signal
import sys
import os

def getToken():
	try :
		tokenLocation = expanduser("~") + "/.rbBot/todoBotToken"
		file = open(tokenLocation, "r", encoding="utf-8")
		token = file.readlines()[0]

		print("*" + token + "*")
		return token
	except:
		print('You have to set the bot token (command : "set-todoBot")')
		exit(1)			

bot = todoBot.telebot.TeleBot(getToken())
database = Database()

fields = {
"Menu" : "Mеnu", "list" : "📃 tаsks", "Back to menu" : "Bаck to mеnu",
"start" : "🏁 stаrt", "settings" : "🔧 sеttings", "add" : "➕ аdd" , 
"Cancel" : "Cаncel",  "options " : "оptiоns ", "delete " : "Dеlete ",
"edit " : "Еdit ", "Name" : "Nаmе", "Description" : "Dеscriptiоn", 
"Time" : "Timе", "Mode" : "Моdе", "Fixed" : "Fixеd", "Floating" : "Flоаting", 
"Back" : "Bасk", "Fix " : "Fіx ", "Flo ":"Flо ", "Fix" : "Fіx", "Flo":"Flо",  
'Default type ' : 'Dеfаult typе ', 'Break the bot' : 'Brеаk the bоt', 
'Back to list' : 'Bаck tо tasks', 'Time settings' : 'Timе sеttings', 
"help" : "Hеlp", "Start" : "Stаrt ", 'Delete all the data' : 'Dеlеtе аll thе dаtа' 
}

fVal = list(fields.values())

# The names are in different encodings.
# I make it to avoid similarities between names of the tasks and the bot buttons 

#													MICROBES
#---------------------------------------------------------------------------------------------------------------------------------------#

tmzn = dbLite(expanduser("~") + "/.rbBot/timezone.db")   #timezone 
tmzn.init()

def addTime(id, time):
	if tmzn.get(id) != []:
		tmzn.delete(id)

	tmzn.add(id, time)
	return 0

def getCurTime(id):
	tm = tmzn.get(id) 
	if tm == []:
		return 0

	return tm[1]

def errGetCurTime(id):
	tm = tmzn.get(id) 
	if tm == []:
		return -1

	return tm[1]

def setTimeHelpMes():
	ret =  """
\tTo set the time type use: 'set : your:current:time'. 
For example:  'set : 22:34' or 'set : 10h 34mPM'
You can also use your county name or country code
"""
	return ret

def digToHumam(taskType):
	if taskType == 1:
		return fields["Flo "]
	else: 
		return fields["Fix "] 

def reverseType(fieldType):
	if fieldType == fields["Fix "]:
		print("to One")
		return 1
	return 0

#													BOTS CELLS
#---------------------------------------------------------------------------------------------------------------------------------------#

def setTime(ftime, id):
	time = toSeconds(ftime)
	myTime = toSeconds( getShortTime() )	
	if time < 0:
		formatErMessage(message.chat.id)
	else:
		new_dist = myTime - time
		changeAllTasksTime(id, new_dist)
		addTime(id, new_dist)
		bot.send_message(id, "Your time was changed to " + ftime)

def menu(id):					# shows the menu
	markup = types.ReplyKeyboardMarkup()	
	markup.row(fields['start'], fields['list'])
	markup.row(fields['add'], fields['settings'])
	bot.send_message(id, "Menu", reply_markup=markup)

def list(id):						# Shows the list 
	keyboard = types.ReplyKeyboardMarkup()
	keyboard.row(fields['Back to menu'])
	n = 1

	temp = database.getB("userID", id)
	if(temp != []):
		for field in temp:
			tType = digToHumam(field[3])
			if tType != "":
				keyboard.row(field[1], tType + str(n), fields['options '] + str(n))
				n = n + 1
			else: 
				print("Wrong type :", field[0], field[1])

	bot.send_message(id, "List", reply_markup=keyboard)

def resTime(id):
	return secToTime( sumTime( toSeconds( getShortTime() ), getCurTime(id) ) )

def botError(id, sError):
	bot.send_message(id, str(sError))	
	menu()

def showEditOptionList(text, userID):
	if text == fields["Name"]:
		database.changeStatus(userID, 5)
		return 5
	elif text == fields["Description"]:
		database.changeStatus(userID, 6)
		return 6
	elif text == fields["Time"]:
		database.changeStatus(userID, 7)
		return 7
	else:
		return -1


def editOption(userID, task, opt, text):
	if opt == 5:
		database.changeField(userID, task, "task", text)
	elif opt == 6:
		database.changeField(userID, task, "desc", text)
	elif opt == 7:	
		time = getTime(text)
		if time < 0:
			formatErMessage(message.chat.id)
		else:
			time = sumTime(time, getCurTime(userID))
			database.changeField(userID, task, "time", time)
	else :
		return -1
	
	database.delD("userID", userID, "task", "|")
	list(userID)
	return 0

def getType(id):
	stat = database.getStatus(id * 2)
	if stat == []:
		database.addStatus(id * 2, 127)
		return 0

	if stat[1] == 126:
		return 1
	return 0

def changeType(id, tType):
	if tType == 1:
		newType = 126
	else:
		newType = 127
	print(newType)
	database.changeStatus(id * 2, newType)	

def changeAllTasksTime(id, dist):
	print("In")
	gap = dist - getCurTime(id)

	temp = database.getB("userID", id)
	if(temp == []):
		return 0
	
	for x in temp:
		if x[3] != 1:
			database.changeField(id, x[1], "time", sumTime(x[4], gap) )

def formatErMessage(id):
	bot.send_message(id, """
Oops, there is something wrong with the format!\n
Needed format: "hh:mm:ss" or (hours)H (mins)M (sec)S
For example: 13:10, 13:10:02
Or 13h 10m, 13h10m.
You can also use PM and AM: 1h10mPM""")

#													BOTS ORGANS
#---------------------------------------------------------------------------------------------------------------------------------------#

def addTaskHandler(text, status):
	if "&" in text:
		bot.send_message(status[0], "You can't use '&'")
		menu(status[0])
		return 1

	if(status[1] == 1): 

		if database.add(status[0], text, "|", getType(status[0]), -1):
			bot.send_message(status[0], "This task already exist")
			database.changeStatus(status[0], 0)	
			menu(status[0])
			return 1

		if text in fVal:
			menu(status[0])
			return 1	

		bot.send_message(status[0], "A description")
		database.changeStatus(status[0], 2)
	
	elif(status[1] == 2):
		t = database.getUncomp(status[0])
		database.changeField(status[0], t[1], "desc",text)

		bot.send_message(status[0], "Notification time")
		database.changeStatus(status[0], 3)
	
	elif(status[1] == 3):
		t = database.getUncomp(status[0])
		time = getTime(text)
		if time < 0:
			formatErMessage(message.chat.id)
		else:
			time_gap = errGetCurTime(status[0]) 
			if time_gap == -1:
				bot.send_message(status[0], "You have to set up the time." + setTimeHelpMes())
				return 1

			time = sumTime(time, time_gap)
			database.changeField(status[0], t[1], "time", time)
	
	return 0

def optionsHandler(text, item):				
	print("Options", item[1])

	if item[1] == 4:
		showEditOptionList(text, item[0])	
		bot.send_message(item[0], "On what to change?")
		return 0

	if item[1] >= 5:
		temp = database.getD("time", -2, "userID", item[0] )
		if temp == []:
			return 1
		temp = temp[0]

		if text == fields['Name'] or text == fields['Time'] or text == fields['Description']:
			return 0 
		
		ret = editOption(item[0], temp[2], item[1], text)
		if ret != -1:
			database.delStatus(item[0])
		return ret
	else:
		return -1

	return 0

def descHandler(text, id):							# Just shows the information about the task
	tasks = database.getUserTasks(id)
	real = database.getRealD("task", text, "userID", id)
	
	if real == []:
		fix = 0
	elif real[0][3] == -1:	
		fix = 0
	else:
		fix = 1

	if text in tasks:
		line = database.getD("task", text, "userID", id)[0]
		left = secToTime( subTime(line[4], toSeconds(getShortTime())))
		time = secToTime( subTime(line[4], getCurTime(id) ) )

		bot.send_message(id, "Task: " + line[1])
		if fix == 0: 
			bot.send_message(id, "Description: " + line[2] + "\nTime: " + time)
		else:
			bot.send_message(id, "Description: " + line[2] + "\nTime: " + time + "\nLeft: " + left)

	return 0

def catchIndexErrors(tasks, text, ind):
	num = int(text[ind : len(text)])

	if num > len(tasks):
		print("The index is too larg")
		return bot_types.FLOATING
	return bot_types.FIXED

def optionsButton(message):
	num = int(message.text[8 : len(message.text)])
	
	markup = types.ReplyKeyboardMarkup()
	markup.row(fields['Back to list'])
	markup.row(fields['delete '] + str(num))
	markup.row(fields['edit '] + str(num))
	markup.row(fields['Start'] + str(num))		
	bot.send_message(message.chat.id, "Options menu", reply_markup=markup)
	
def deleteButton(message):
	userTasks = database.getUserTasks(message.chat.id)
	num = int(message.text[7 : len(message.text)])

	database.delD("userID", message.chat.id, "task", userTasks[num - 1])
	list(message.chat.id)
	

def editButton(message):
	userTasks = database.getUserTasks(message.chat.id)
	num = int(message.text[5 : len(message.text)])

	keyboard = types.ReplyKeyboardMarkup()
	keyboard.row(fields['Cancel'])
	keyboard.row(fields['Name'])
	keyboard.row(fields['Description'])
	keyboard.row(fields['Time'])
	
	bot.send_message(message.chat.id, "What to change?", reply_markup=keyboard)
	database.addStatus(message.chat.id, 4)
	database.cAdd(message.chat.id, "|" , userTasks[num - 1], 2, -2)


def start_task(message):
	userTasks = database.getUserTasks(message.chat.id)
	num = int(message.text[6 : len(message.text)])
	database.startOne(message.chat.id, userTasks[num - 1])
	list(message.chat.id)

def fix_floButton(message):
	userTasks = database.getUserTasks(message.chat.id)
	num = int(message.text[4 : len(message.text)])
	
	database.changeField(message.chat.id, userTasks[num - 1], "type", reverseType(message.text[0 : 4]) )
	list(message.chat.id)


def otherMessages(message):
	temp = database.getStatus(message.chat.id)
	print("Here. Status :  ", temp)

	if temp != []:
		if temp[1] <= 3:
			addTaskHandler(message.text, temp)
		elif database.getStatus(message.chat.id) == 10:
			if inTz(message.text):
				setTime(getTzShortTime(message.text), message.chat.id)
			else:
				bot.send_message(message.chat.id, "Timezone not found")

			database.delStatus(message.chat.id)	
		elif temp[1] >= 4:
			optionsHandler(message.text, temp)
	else:
		descHandler(message.text, message.chat.id)

def cleanItUp(id):
	database.delD("userID", id, "time", -2)
	database.delD("userID", id, "task", "|")
	database.delU(id)
	database.delStatus(id)

def settingsButton(id):
	keyboard = types.ReplyKeyboardMarkup()
	keyboard.row(fields['Back to menu'])
	keyboard.row(fields['Default type '] + digToHumam( getType(id) ) )
	keyboard.row(fields['Time settings'])
	keyboard.row(fields['Delete all the data'])
	keyboard.row(fields['help'])
	#keyboard.row(fields['Break the bot'])
	
	bot.send_message(id, "Settings", reply_markup=keyboard)

def timeSettingMessage(id):
	resGap = errGetCurTime(id)

	if resGap == -1:
		mes = "Your current time is unknow"
	else:
		mes = "Your current time is: " +  resTime(id)
		
	bot.send_message(id, mes + setTimeHelpMes())

def tzSelector(tz_lst):
	keyboard = types.InlineKeyboardMarkup()

	for x in tz_lst:
		keyboard.row(x)

	bot.send_message(message.chat.id, "What is your timezone?", reply_markup=keyboard)

#													BOTS BODY
#---------------------------------------------------------------------------------------------------------------------------------------#

@bot.message_handler(commands=["help"])
def help_msg(message):
	help_message = """
There are two types of tasks: fixed and floating.
Fixed tasks will send you a notification every day until you delete the task. 
With floating tasks, you have to activate them using the 'start' button. It works like a timer and after some time it'll send you a notification.
You can change the type of the task in the task list, also in the options you can start one particular task and not all of them at once.
"""
	bot.send_message(message.chat.id, help_message)

def thereIsNoTime(id):
	if errGetCurTime(id) == -1:
		return 1
	return 0
	
def timeSettings(id, mes):
	if inCountries(mes):
		tz_lst = getTzList(getCountryCode(mes))
		if len(tz_lst) == 1:
			setTime(getTzShortTime(tz_lst[0]), id)
		else:
			database.addStatus(id, 10)
			tzSelector(tz_lst)
		
	elif inTzCodes(mes):
		tz_lst = getTzList(mes)
		if len(tz_lst) == 1:
			print(getTzShortTime(tz_lst[0]))
			setTime(getTzShortTime(tz_lst[0]), id)

		else:
			database.addStatus(id, 10)
			tzSelector(tz_lst)

	else:
		time = getTime(mes)

		if time < 0:
			bot.send_message(id, "Oops, there is something wrong with the format!" + setTimeHelpMes() )				
			return -1
		else:	
			setTime(time, id)
		
	timeSettingMessage(id)

@bot.message_handler(commands=["start"])
def start_msg(message):
	help_msg(message)
	bot.send_message(message.chat.id, "What time is it for you?" + setTimeHelpMes())
	menu(message.chat.id)

@bot.message_handler(content_types=["text"])
def bot_messages(message):
	database.updateRealTable()
	if database.showRealTable() == []:
		database.addAllTasks()

	# It is needed to delete trash from the database
	if(																	### cleaning		
		message.text == fields['Menu'] or 
		message.text == fields['Back to menu'] or
		message.text == fields['list'] or message.text == fields["add"] or
		message.text == fields['settings'] or message.text == fields["start"] or 
		message.text == fields["Cancel"]
		):
		print("Command")
		cleanItUp(message.chat.id)		
	
	if message.text[0 : 6] == "set : ":
		mes = message.text[6 : len(message.text)]
		timeSettings(message.chat.id, mes)

	elif thereIsNoTime(message.chat.id) and database.getStatus(message.chat.id) != 10:
		try:
			timeSettings(message.chat.id, message.text)
		except:
			bot.send_message(message.chat.id, "There is some error" + setTimeHelpMes())
	
	elif (																### Menu
		message.text == fields['Menu'] or 
		message.text == fields['Back to menu'] or 
		message.text == fields["Cancel"]
		):
		menu(message.chat.id)

	elif message.text == fields['list'] or message.text == fields['Back to list'] :		### List
		list(message.chat.id)
	
	elif message.text == fields['start']:								### Start
		database.start(message.chat.id)
		bot.send_message(message.chat.id, "Timer started!")
		
	elif message.text == fields['add']:									### Add
		database.addStatus(message.chat.id, 1)
		bot.send_message(message.chat.id, "Okey! Give your task a short name")

	elif message.text == fields['settings']:							### Settings
		settingsButton(message.chat.id)
	
	elif message.text[0 : 8] == fields["options "]:						### Options
		optionsButton(message)
	
	elif message.text[0 : 7] == fields["delete "]:						### Delete
		deleteButton(message)
	
	elif message.text[0 : 5] == fields["edit "]:						### Edit
		editButton(message)
	
	elif message.text[0 : 4] == fields["Flo "] or message.text[0 : 4] == fields["Fix "]:  ## Fix or Flo button
		fix_floButton(message)
	
	elif message.text[0 : 13] == fields['Default type ']:
		
		if fields["Fix"] == message.text[13 : 16]:	
			changeType(message.chat.id, 1)
			print( getType(message.chat.id) )
		else :
			changeType(message.chat.id, 0)

		settingsButton(message.chat.id)

	#elif message.text == fields['Break the bot']:				# debug purposes only
	#	database.delUN(message.chat.id)
								
	elif message.text[0 : 6] == fields["Start"]:						### start one tasks
		start_task(message)

	elif message.text == fields["Time settings"]:
		timeSettingMessage(message.chat.id)

	elif message.text == fields["help"]:
		help_msg(message)
	
	elif message.text == fields["Delete all the data"]:
		database.delB("userID", message.chat.id)
		bot.send_message(message.chat.id, "All data deleted")

	else:																### Others
		print(message.text)
		otherMessages(message)

#													THE HEAD!!!!!
#---------------------------------------------------------------------------------------------------------------------------------------#

def checkToken():
	if bot_variables.token == '':
		print('You have to registrate your bot (command : "set-todoBot")')
		exit(1)	

def signal_handler(sig, frame):
	database.updateRealTable()
	print('\nExit!')
	sys.exit(0)

def fixDataBase():
	table = database.showRealTable()
	res = []

	for x in table:
		if not (now() - x[4]) < 60 * 60:
			res.append(x)

	if res == []:
		return 0

	database.commitReal(table = res)
	database.addAllTasks()

def cleanDataBases():
	database.dropTemp()
	database.dropTable()
	database.dropRealTable()

def startBot():
	if os.name != "posix":
		os.system("chcp 65001")
		
	if len(sys.argv) > 1:
		if sys.argv[1] == '--clean' or sys.argv[1] == '-c':
			print("Heeeeelp") 
			cleanDataBases()
			exit(0)
	
	fixDataBase()

	print("Start")
	while True:
		signal.signal(signal.SIGINT, signal_handler)
		try:
			print("Polling")
			bot.polling(none_stop=True, interval=1, timeout=2)
		except Exception as e:
			time.sleep(5)
		except KeyboardInterrupt:
			exit(0)
