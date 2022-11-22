# importing the necessary dependencies
from flask import Flask, request,render_template
import numpy as np
import pandas as pd
import pickle
import os

model = pickle.load(open('flightdelay.pkl','rb'))
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predicition',methods =['POST'])
def predict() :
    if request.method=="POST":
        name=request.form["name"]
        month=request.form["month"]
        dayofmonth = request.form['dayofmonth']
        dayofweek = request.form['dayofweek']
        origin = request.form['origin']
        destination=request.form['destination']

        origin1,origin2,origin3,origin4,origin5=0,0,0,0,0
        if(origin=="msp"):
            origin1,origin2,origin3,origin4,origin5=0,0,0,1,0
        if(origin=="dtw"):
            origin1,origin2,origin3,origin4,origin5=0,1,0,0,0
        if(origin=="jfk"):
            origin1,origin2,origin3,origin4,origin5=0,0,1,0,0
        if(origin=="sea"):
            origin1,origin2,origin3,origin4,origin5=0,0,0,0,1
        if(origin=="alt"):
            origin1,origin2,origin3,origin4,origin5=1,0,0,0,0


        if(destination == "msp"):
            destination1,destination2,destination3,destination4,destination5 = 0,0,0,0,1
        if(destination == "dtw"):
            destination1,destination2,destination3,destination4,destination5 = 1,0,0,0,0
        if(destination == "jfk"):
            destination1,destination2,destination3,destination4,destination5 = 0,0,1,0,0
        if(destination == "sea"):
            destination1,destination2,destination3,destination4,destination5 = 0,1,0,0,0
        if(destination == "alt"):
            destination1,destination2,destination3,destination4,destination5 = 0,0,0,1,0
        dept = request.form['dept']
        arrtime = request.form['arrtime']
        actdept = request.form['actdept']
        depti5=int(dept)-int(actdept)
        total = [[month,dayofmonth,dayofweek,origin1,origin2,origin3,origin4,origin5,destination1,destination2,destination3,destination4,destination5,dept,actdept,depti5,arrtime]]

        y_pred = model.predict(total)

        print(y_pred)

        if(y_pred==[0.]):
            return "The Flight will be on time"
        else:
            return "THE FLIGHT WILL BE DELAYED"

app.run(debug=True)
    
