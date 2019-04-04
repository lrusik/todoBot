#!/usr/bin/python3

import os
from os.path import expanduser

dbName =  expanduser("~") + "/.rbBot/toDoList.db"    # yakushev hui

def getTable():
    ret = list()
   
    try:
        file = open(dbName, "r", encoding="utf-8")
        text = file.readlines()   
        for temp in text:
            words = temp.split('&')
            ret.append([int(words[0]), words[1], words[2], int(words[3]), int(words[4])])
        
    except Exception as e:
        print("Error : " + str(e))
        file = open(dbName, "w+")

    file.close()
    return ret

def rdb_sort(table):
    res = table
    for i in range(len(res)):
        for j in range(len(res) - 1):
            if res[i][4] < res[j][4]:
                temp = res[i]
                res[i] = res[j]
                res[j] = temp
    return res

def write_table(table):
    file = open(dbName, "w", encoding="utf-8")

    table = rdb_sort(table)
    
    for item in table:
        file.write("%i&%s&%s&%i&%i\n" % (item[0], item[1], item[2], item[3], item[4]))

    file.close()

