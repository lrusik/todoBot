#!/usr/bin/python3

#														BOTS WATCH
#---------------------------------------------------------------------------------------------------------------------------------------#

import time
import pytz
from datetime import datetime
from iso3166 import countries

oneDay = 60 * 60 * 24

def nStr(num):
	if num >= 0 and num <=9 :
		return "0" + str(num)
	return str(num)

def toSeconds(time):             # transfer the regular time format to seconds
	hour = int(time[0 : 2]) 
	mint = int(time[3 : 5])
	sec  = int(time[6 : 8])

	if time == "24:00:00":
		return 60 * 60 * 24

	if(hour > 23 or mint >= 60 or sec >= 60):
		return -1

	return hour * 60 * 60 + mint * 60 + sec

def getShortTime():
	return str(datetime.now())[11:19]

def daysInMonth(month):
	monthArr = [0, 
	31, 28, 31, 
	30, 31, 30, 
	31, 31, 30, 
	31, 30, 31
	]
	
	year = str(datetime.now())[0:4]
	if month == 2 and int( year ) % 4 == 0:
		return 29
	
	return monthArr[month] 

def toSec(time):
	month = int(time[0 : 2])
	day   = int(time[3 : 5])
	sec = toSeconds( time[6 : 14] )

	if month < 1 or month > 12:
		return -1

	if day < 1 or day > daysInMonth(month):
		return -1

	if sec == -1:
		return -1

	return sec + day * 24 * 60 * 60

def sNow():
	return str(datetime.now())[5:19]

def now():
	return toSec( sNow() )

def today():
	return now() - toSeconds( getShortTime() )

def todayIn(Time):
	return today() + Time

def tomorrow():
	return today() + oneDay

def tomorrowIn(Time):
	return tomorrow() + Time

	
def timeTail(tTime):
	if tTime > 60 * 60 * 24:
		tTime = tTime - (60 * 60 * 24)
	return	tTime

def secToTime(time):			#The opposite of toSeconds
	hour = int( time / (60 * 60) )
	mint = int( time % (60 * 60)  / 60 )
	sec  = int( (time % 60) ) 

	if time > (60 * 60 * 24) or time < 0:
		return ""

	return nStr(hour) + ":" + nStr(mint) + ":" + nStr(sec)

def dSecToTime(time):
	day  = int( time / (60 * 60 * 24) ) 
	dayTime = time % (60 * 60 * 24)
	hour = int( dayTime / (60 * 60))
	mint = int( dayTime % (60 * 60)  / 60)
	sec  = int( dayTime % 60 ) 

	if time > (32 * 60 * 60 * 24) or time < 0:
		return ""

	return nStr(day) + "-" + nStr(hour) + ":" + nStr(mint) + ":" + nStr(sec)

def caclTime(gTime):
	return timeTail( toSeconds( str( datetime.now() )[11:19] ) + gTime )

def sumTime(time, dist):
	time += dist
	if time > 24 * 60 * 60:
		time -= 24 * 60 * 60
	elif time < 0:
		time = 24 * 60 * 60 + time

	return time

def subTime(time, dist):
	return sumTime(time, -1 * dist)

def resTime(id):
	return secToTime( sumTime( toSeconds( getShortTime() ), getCurTime(id) ) )

def AmPm(hours, form):
	if hours > 12 or hours <= 0:
		return -1

	if hours == 12:
		if form == 0:
			return 0
		return 12
	
	if form == 1:
		return hours + 12
	
	return hours

def timeToSFormat(lst, form):
	if len(lst) < 2:
		return -1
	
	hours = int(lst[0])
	if form != -1:
		hours = AmPm(hours, form)

	if len(lst) == 2:
		return nStr(hours) + ":" + nStr(int(lst[1])) + ":" + "00"  

	if len(lst) == 3:
		return nStr(hours) + ":" + nStr(int(lst[1])) + ":" + nStr(int(lst[2]))  

	return -1 

def pmOrAm(text):
	am = ["AM", "am", "Am", "aM"]
	pm = ["PM", "pm", "Pm", "pM"]
	
	for x in am:
		if x in text:
			return 0

	for x in pm:
		if x in text:
			return 1
	
	return -1

def delExtraChar(text):
	try :
		text = text.replace('\n', '')
		text = text.replace(' ', '')
	except:
		pass

	return text

def getAllNonNumChars(text):
	ret = ''
	for x in text:
		if not (x <= '9' and x >= '0'):
			ret += x
	
	return ret

def literalType(Time):	
	times = getAllNonNumChars(Time)
	res = ['', '', '']
	
	for x in times:
		temp = Time.split(x)
		Time = temp[1]
		
		if (x == 'h' or x == 'H') and res [0] == '':
			res[0] = temp[0]
		elif (x == 'm' or x == 'M') and res[1] == '':
			res[1] = temp[0]
		elif (x == 's' or x == 'S') and res[2] == '':
			res[2] = temp[0]
		else:
			return -1

	if res[0] == '' and res[1] == '' and res[2] == '':
		return -1 

	if res[0] == '':
		res[0] = '0'
	if res[1] == '':
		res[1] = '0'
	if res[2] == '':
		res[2] = '0'
	
	return res

def getTime(Time):
	Time = delExtraChar(Time)
	
	try:
		form = pmOrAm(Time)
		print("0")
		print(form, Time)
		if form != -1:
			Time = Time[0:-2]
			print("1")
			print(Time)

		if ":" in Time:
			timeLst = Time.split(':')
			print("2")
			print(timeLst)
		else:
			timeLst = literalType(Time)
			print("3")
			print(timeLst)
		print("out")
		return toSeconds( timeToSFormat(timeLst, form) )
	except:
		return -1

def getCountryCode(country):
	for x in countries:
		if x[0] == country:
			return x[1]

	return ""

def getTzList(code):
	return pytz.country_timezones[code]

def getTzTime(timezone):
	tz = pytz.timezone(timezone)
	return datetime.now(tz)

def inCountries(country):
	for x in countries:
		if x[0] == country:
			return True

	return False

def inTzCodes(tz):
	tz = tz.upper()
	for x in countries:
		if x[1] == tz or x[2] == tz:
			return True

	return False

def inTz(timezone):
	for x in countries:
		try:
			if timezone in getTzList(x[1]):
				return True
		except:
			pass

	return False 
	
def getTzShortTime(tz):
	return str(getTzTime(tz))[11:19]

if __name__ == "__main__":
	print(getTime("20")	)	

