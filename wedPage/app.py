from flask import Flask, request, render_template
from utils import *
from api import *
import requests
import numpy as np


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('visual_data.html')

@app.route('/carHome')
def car_home():
    reqCarHome = databaseRequest("carHome",conversension_car)
    array = np.array(reqCarHome["data"])
    return render_template('show_data.html',data=reqCarHome["data"], names=reqCarHome["names"],success=reqCarHome["success"],fail=reqCarHome["fail"], dist=reqCarHome['dist']
    ,mean=round(array.mean(),2),std=round(array.std(),2))

@app.route('/quickQuote')
def quickQuote():
    reqQuickQuote = databaseRequest("quickQuote",conversension_quick_quote)
    array = np.array(reqQuickQuote["data"])
    return render_template('show_data.html',data=reqQuickQuote["data"], names=reqQuickQuote["names"],
    success=reqQuickQuote["success"],fail=reqQuickQuote["fail"],dist=reqQuickQuote['dist'],mean=round(array.mean(),2),std=round(array.std(),2))

@app.route('/investment')
def investment():
    reqInvestment = databaseRequest("investment",conversension_id)
    array = np.array(reqInvestment["data"])
    return render_template('show_data.html',data=reqInvestment["data"], names=reqInvestment["names"],
    success=reqInvestment["success"],fail=reqInvestment["fail"],dist=reqInvestment['dist'],mean=round(array.mean(),2),std=round(array.std(),2))

@app.route('/delete', methods=['POST'])
def delete():
    number =  int(request.form['number'])
    print(number)
    tables = ["carHome", "quickQuote", "investment"]
    answer = {"operation":False}
    if number == 3:
        for name in tables:
            delete_table(name)
        answer['operation'] = True
    elif 0 <= number < 3:
        delete_table(tables[number])
        answer['operation'] = True
    return answer

if __name__ == '__main__':
    app.run(debug = True)