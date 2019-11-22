from flask import Flask, request, render_template
from utils import *
from api import *
import requests


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('visual_data.html')

@app.route('/carHome')
def car_home():
    reqCarHome = databaseRequest("carHome",conversension_car)
    return render_template('show_data.html',data=reqCarHome[1], names=reqCarHome[0])

@app.route('/quickQuote')
def quickQuote():
    reqQuickQuote = databaseRequest("quickQuote",conversension_quick_quote)
    return render_template('show_data.html',data=reqQuickQuote[1], names=reqQuickQuote[0])

@app.route('/investment')
def investment():
    reqInvestment = databaseRequest("investment",conversension_id)
    return render_template('show_data.html',data=reqInvestment[1], names=reqInvestment[0])

@app.route('/delete', methods=['POST'])
def delete():
    number =  request.form['number']
    tables = ["carHome", "quickQuote", "investment"]
    if number == 4:
        for name in tables:
            sql_delete_table(name)
    return {"operation":sql_delete_table(tables[int(number)])}

if __name__ == '__main__':
    app.run(debug = True)