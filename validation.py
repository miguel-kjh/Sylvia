from rasa_nlu.model import Metadata, Interpreter
import matplotlib.pyplot as plt
from utils import *
import numpy as np
import requests
import re

def connection(mess) -> dict:
    data = {
        "message_id": "b2831e73-1407-4ba0-a861-0f30a42a42a2a5a",
        "text": mess,
        "sender": "user"
    }
    r = requests.post(url = "http://localhost:5005/model/parse", json = data, headers={'Content-Type': 'application/json'}) 
    data = r.json()
    return data

def validationConvesations(data:dict, name:str):
    x1 = []
    y1 = []
    succes = 0
    fail = 0
    print("Fails", name)
    for conv in data.keys(): 
        awnser = connection(data[conv][0])
        x1.append(conv)
        if re.sub(r'-\d','',conv) == awnser['intent']['name']:
            succes += 1
            y1.append(awnser['intent']['confidence'])
        else:
            print("Label: ", conv,  "Awnser:", awnser['intent']['name'])
            fail += 1
            y1.append(0.0)
    print("----------------------------")
    print("mean:", np.mean(y1))
    print("accuracy:", succes*100/(succes+fail))
    plt.bar(np.arange(2),[succes,fail])
    plt.xticks(np.arange(2), ('Succes','Fail'))
    plt.savefig('graph/bar_'+ name +'.png')
    plt.close()

    plt.plot(x1,y1,marker='o', linestyle='--')
    plt.ylim(0,1)
    plt.xticks(rotation=75)
    plt.savefig('graph/plot_'+ name +'.png')
    plt.close()


if __name__ == "__main__":    
    validationConvesations(conversension_car, "Car_Home")
    validationConvesations(conversension_id, "inv")
    validationConvesations(conversension_quick_quote, "quick_quote")