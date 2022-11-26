# importing the necessary dependencies
from flask import Flask, request,render_template
import numpy as np
import pandas as pd
import pickle
import requests
import json

# model = pickle.load(open('flightdelay.pkl','rb'))
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

        # y_pred = model.predict(total)

        # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
        API_KEY = "IU_76Xzg4uhR9DbnmjkoLeMoa5ePG3QAmmPfcUBPjziH"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
        API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]

        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"field": [["f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15","f16"]], "values": total}]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/9b151467-653e-419b-bb25-1b3a6c11228d/predictions?version=2022-11-22', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())

        y_pred=response_scoring.json()

        print(y_pred['predictions'][0]['values'][0][1][1])

        v=y_pred['predictions'][0]['values'][0][0]
        print(type(v))

        if(v==0.):
            return "The Flight will be on time"
        else:
            return "THE FLIGHT WILL BE DELAYED"

app.run(debug=True)
    
