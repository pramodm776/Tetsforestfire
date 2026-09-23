import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns

from flask import Flask,request,jsonify,render_template

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / 'models' / 'ridge.pkl', 'rb') as model_file:
    ridge_model = pickle.load(model_file)

with open(BASE_DIR / 'models' / 'scaler.pkl', 'rb') as scaler_file:
    standard_scaler = pickle.load(scaler_file)


application = Flask(__name__)
app = application

@app.route("/", methods =['GET', 'POST'])
def predict_datapoint():
    
    if request.method=="POST":
        Temperature = float(request.form.get('Temperature'))
        RH = float(request.form.get('RH'))
        Ws = float(request.form.get('Ws'))
        Rain = float(request.form.get('Rain'))
        FFMC = float(request.form.get('FFMC'))
        DMC = float(request.form.get('DMC'))
        ISI = float(request.form.get('ISI'))
        Classes = float(request.form.get('Classes'))
        Region = float(request.form.get('Region'))
        
        new_data_scaled=standard_scaler.transform([[Temperature,RH,Ws,Rain,FFMC,DMC,ISI,Classes,Region]])
        result = ridge_model.predict(new_data_scaled)      
        
        return render_template('home.html',result=result[0])
        
        
        
        
        
    else:
        return render_template('home.html')
    

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    )