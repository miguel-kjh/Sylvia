import re
import numpy as np
import sqlite3
import requests
from typing import *
from connection import DB_connection
from utils import load,save

def connection(mess:str) -> dict:
    data = {
        "message_id": "b2831e73-1407-4ba0-a861-0f30a42a42a2a5a",
        "text": mess,
        "sender": "user"
    }
    r = requests.post(url = "http://localhost:5005/model/parse", json = data, headers={'Content-Type': 'application/json'}) 
    data = r.json()
    return data

def databaseRequest(name:str, conversension: dict) -> tuple:
    con = DB_connection()
    sentence = "SELECT count(id) FROM "+ name + ";"
    con.cursorObj.execute(sentence)
    amountOfData = con.cursorObj.fetchone()[0]
    print(amountOfData)
    if amountOfData == 0:
        req = validationConversations(conversension)
        save(name,req['dist'])
        result = req
        con.sql_insert_rate(req["fail"], req["success"],name)
        for intentcion,data in zip(req["names"],req["data"]):
            print((intentcion,data))
            con.sql_insert((intentcion,data),name)
        return result
    else:
        sentence = "select name,data from " + name + ";"
        con.cursorObj.execute(sentence)
        rows = con.cursorObj.fetchall()
        intentions = []
        confiances = []
        for intention,confiance in rows:
            intentions.append(intention)
            confiances.append(confiance)
        sentence = "select fail,success from rate where conversation='"+name+"';"
        print(sentence)
        con.cursorObj.execute(sentence)
        obj = con.cursorObj.fetchall()[0]
        print(obj)
        return {
            "names":intentions,
            "data":confiances,
            "fail":obj[0],
            "success":obj[1],
            "dist":load(name)
        }

def validationConversations(data:dict) -> dict:
    x1 = []
    y1 = []
    dist = {}
    succes = 0
    fail = 0
    for conv in data.keys(): 
        list_values = []
        x1.append(conv)
        for example in data[conv]:
            awnser = connection(example)
            dist[awnser['intent']['name']] = {
                "intentions":[i['name'] for i in awnser['intent_ranking']],
                "pred":[round(i['confidence'],5) for i in awnser['intent_ranking']]
            }
            if re.sub(r'-\d','',conv) == awnser['intent']['name']:
                succes += 1
                list_values.append(round(awnser['intent']['confidence'],2))
            else:
                #print(awnser)
                print("Label: ", conv,  "Awnser:", awnser['intent']['name'], "with", example)
                fail += 1
                list_values.append(0.0)
        y1.append(np.mean(list_values))
    return {
        "names":x1,
        "data":y1,
        "fail":round(100*fail/(fail+succes)),
        "success":round(100*succes/(fail+succes)),
        "dist":dist
    }

def delete_table(name:str):
    con = DB_connection()
    con.sql_delete_table(name)