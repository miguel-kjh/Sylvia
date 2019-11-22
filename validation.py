import matplotlib.pyplot as plt
from utils import *
import numpy as np
import requests
import re
import seaborn as sn
import pandas as pd

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
        list_values = []
        x1.append(conv)
        for example in data[conv]:
            awnser = connection(example)
            if re.sub(r'-\d','',conv) == awnser['intent']['name']:
                succes += 1
                list_values.append(awnser['intent']['confidence'])
            else:
                print("Label: ", conv,  "Awnser:", awnser['intent']['name'], "with", example)
                fail += 1
                list_values.append(0.0)
        y1.append(np.mean(list_values))
            
    print("----------------------------")
    print("mean:", np.mean(y1))
    print("accuracy:", succes*100/(succes+fail))
    df = pd.DataFrame({'y': [succes,fail]},
                   index=['success', 'fail'])
    plot = df.plot.pie(y='y', figsize=(5, 5))
    print(plot)

    plt.plot(x1,y1,marker='o', linestyle='--')
    plt.ylim(0,1)
    plt.xticks(rotation=75)
    plt.savefig('graph/plot_'+ name +'.png')
    plt.close()


if __name__ == "__main__":    
    #validationConvesations(conversension_car, "Car_Home")
    #validationConvesations(conversension_id, "inv")
    #validationConvesations(conversension_quick_quote, "quick_quote")
    results = [{} for i in target_intent.keys()]
    for index in range(len(target_intent.keys())):
        for i in target_intent.keys():
            results[index][i] = 0.0 
    for index,i in enumerate(target_intent.keys()):
        awnser = connection(target_intent[i])
        for j in awnser["intent_ranking"]:
            results[index][j['name']] = round(j['confidence'],2)
    array = []
    for i in range(len(results)):
        array.append(list(results[i].values()))
    df_cm = pd.DataFrame(array, range(len(array)),range(len(array)))
    sn.set(font_scale=1.4)#for label size
    sn.heatmap(df_cm,annot=True)
    plt.show()
