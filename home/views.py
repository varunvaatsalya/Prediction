import json
import os
from django.shortcuts import render
import pickle
import numpy as np


model_path = os.path.join(os.path.dirname(__file__), 'model', 'model.pickle')
with open(model_path, 'rb') as file:
    model = pickle.load(file)


json_path = os.path.join(os.path.dirname(__file__), 'columns.json')
with open(json_path, 'r') as file:
    columns_data = json.load(file)


locations = columns_data['data_columns'][3:]

def get_predict(request):
    prediction = None

    if request.method == 'POST':
        
        location = request.POST.get('location')
        sqft = float(request.POST.get('sqft'))
        bath = int(request.POST.get('bath'))
        bhk = int(request.POST.get('bhk'))


        price = predict_price(location, sqft, bath, bhk)
        prediction = round(price, 3)
    return render(request, 'home.html', {'locations': locations, 'prediction': prediction})

def predict_price(location, sqft, bath, bhk):
    loc_index = np.where(np.array(columns_data['data_columns']) == location)[0][0]
    x = np.zeros(len(columns_data['data_columns']))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    return model.predict([x])[0]
