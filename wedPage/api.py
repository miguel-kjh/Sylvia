import re
import numpy as np
import sqlite3

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

def sql_delete_table(name:str) -> bool:
    con = sqlite3.connect('wedPage/dataBase.db')
    cursorObj = con.cursor()
    cursorObj.execute("DELETE FROM "+name+";")
    con.commit()
    con.close()
    return True

def sql_delete_all(name:str) -> bool:
    pass

def databaseRequest(name:str, conversension: dict) -> tuple:
    con = sqlite3.connect('wedPage/dataBase.db')
    sentence = "SELECT count(id) FROM "+ name + ";"
    cursorObj = con.cursor()
    cursorObj.execute(sentence)
    amountOfData = cursorObj.fetchone()[0]
    print(amountOfData)
    if amountOfData == 0:
        req = validationConversations(conversension)
        result = req
        for intentcion,data in zip(req[0],req[1]):
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
        con.close()
        return intentions,confiances

def validationConversations(data:dict) -> tuple:
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
    return x1,y1