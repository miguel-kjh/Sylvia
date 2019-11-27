import re
import numpy as np
import sqlite3
import requests


def connection(mess) -> dict:
    data = {
        "message_id": "b2831e73-1407-4ba0-a861-0f30a42a42a2a5a",
        "text": mess,
        "sender": "user"
    }
    r = requests.post(url = "http://localhost:5005/model/parse", json = data, headers={'Content-Type': 'application/json'}) 
    data = r.json()
    return data

def sql_insert(con, entities, nameTable):
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO '+ nameTable +'(name, data) VALUES(?, ?)', entities)
    con.commit()

def sql_delete_table(name:str):
    con = sqlite3.connect('dataBase.db')
    cursorObj = con.cursor()
    cursorObj.execute("DELETE FROM "+name+";")
    con.commit()
    con.close()

def sql_insert_rate(con,fail,success,name):
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO rate(conversation, fail, success) VALUES(?, ?, ?)', (name,fail,success))
    con.commit()

def databaseRequest(name:str, conversension: dict) -> tuple:
    con = sqlite3.connect('dataBase.db')
    sentence = "SELECT count(id) FROM "+ name + ";"
    cursorObj = con.cursor()
    cursorObj.execute(sentence)
    amountOfData = cursorObj.fetchone()[0]
    print(amountOfData)
    if amountOfData == 0:
        req = validationConversations(conversension)
        result = req
        sql_insert_rate(con,req["fail"], req["success"],name)
        for intentcion,data in zip(req["names"],req["data"]):
            print((intentcion,data))
            sql_insert(con,(intentcion,data),name)
        con.close()
        return result
    else:
        sentence = "select name,data from " + name + ";"
        cursorObj.execute(sentence)
        rows = cursorObj.fetchall()
        intentions = []
        confiances = []
        for intention,confiance in rows:
            intentions.append(intention)
            confiances.append(confiance)
        sentence = "select fail,success from rate where conversation='"+name+"';"
        print(sentence)
        cursorObj.execute(sentence)
        obj = cursorObj.fetchall()[0]
        print(obj)
        con.close()
        return {
            "names":intentions,
            "data":confiances,
            "fail":obj[0],
            "success":obj[1]
        }

def validationConversations(data:dict) -> dict:
    x1 = []
    y1 = []
    succes = 0
    fail = 0
    for conv in data.keys(): 
        list_values = []
        x1.append(conv)
        for example in data[conv]:
            awnser = connection(example)
            if re.sub(r'-\d','',conv) == awnser['intent']['name']:
                succes += 1
                list_values.append(round(awnser['intent']['confidence'],2))
            else:
                print("Label: ", conv,  "Awnser:", awnser['intent']['name'], "with", example)
                fail += 1
                list_values.append(0.0)
        y1.append(np.mean(list_values))
    
    return {
        "names":x1,
        "data":y1,
        "fail":round(100*fail/(fail+succes)),
        "success":round(100*succes/(fail+succes))
    }