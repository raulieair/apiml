from flask import Flask,request,jsonify
import pickle
import pandas as pd
import numpy as np
from model_db import entry
import db

from model import train

#Iniciar app de flask
app = Flask(__name__)



@app.route('/predict', methods=["POST"])
def predict():
    #Cargar modelo
    model = pickle.load(open('models/decisiontree.pkl',"rb"))

    #Recogida json recibida por la api
    data_json = request.json

    #Lista para guardar arrays a predecir
    data_predict = []

    #Recorro los elementos del json creando los arrays para cada uno y añadiendolo a la lista a predecir
    for i in range(0,len(data_json)):
        data_send = np.array([value for value in data_json[i].values()])
        data_predict.append(data_send)
 

    prediction = model.predict(data_predict)   #Predicción de los casos recibidos 
    return jsonify({"Prediction":list(prediction)})


@app.route('/add_entry', methods=["POST"])
def add_entry():
    data_json = request.json  
    
    for i in range(0,len(data_json)):
        data_send = np.array([value for value in data_json[i].values()])
        print(i,type(data_send))
        
    #por cada elemento del json recibido creamos una fila en nuestra base de datos
        entries = entry(sepal_length=data_send[0],sepal_width=data_send[1],petal_length=data_send[2],petal_width=data_send[3],specie=data_send[4])
        
        db.session.add(entries)
        db.session.commit()

    return "Added correctly"

@app.route('/train', methods=["POST"])
def train_model():
    file = request.files['']
    model, accuracy = train(file)

    pickle.dump(model,open('models/decisiontree.pkl','wb'))
    return jsonify({"Accuracy":accuracy}), 200


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)