from flask import Flask,request,jsonify,session

import numpy as np
from model_db import entry, User
import db
from model import train
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity

import mlflow


#Iniciar app de flask
app = Flask(__name__)

app.config['SECRET_KEY'] = '123456abc'
jwt = JWTManager(app)

#Diccionario con usuarios ejemplo para la autenticación
'''user = {
    'username': 'admin',
    'password': '1234'
}'''


@app.route('/token', methods=["POST"])
def create_token():

    username = request.json.get("username")
    password = request.json.get("password")
    user = db.session.query(User).filter_by(username=username,password=password).first()

    if user is None:
        return jsonify({'message': 'Falied username or password'})
    
    # Create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id }), 200



@app.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    
    return jsonify({"Id usuario": user.id, "username": user.username }), 200



@app.route('/predict', methods=["POST"])
@jwt_required()
def predict():
    #Cargar modelo
    #model = pickle.load(open('models/decisiontree.pkl',"rb"))
    # Get the MLflow tracking URI
    mlflow_tracking_uri = mlflow.get_tracking_uri()

    # Use the tracking URI to build the model URI
    latest_run = mlflow.search_runs(order_by=["start_time desc"]).iloc[0]
    model_uri = f"{mlflow_tracking_uri}/0/{latest_run.run_id}/artifacts/decision_tree_model"
    
    
    model = mlflow.sklearn.load_model(model_uri)
    
    #Recogida json recibida por la api
    data_json = request.json
    
    if type(data_json)==list:
        try:
            #Lista para guardar arrays a predecir
            data_predict = []

            #Recorro los elementos del json creando los arrays para cada uno y añadiendolo a la lista a predecir
            for i in range(0,len(data_json)):
                data_send = np.array([value for value in data_json[i].values()])
                data_predict.append(data_send)
        

            prediction = model.predict(data_predict)   #Predicción de los casos recibidos 
            result=jsonify({"Prediction":list(prediction)}),200
            
        except ValueError:
            result = "The model expecting 4 features as input",400
            

    else:
        result="Error input type: list required",400
        
    return result


@app.route('/add_entry', methods=["POST"])
@jwt_required()
def add_entry():  
    data_json = request.json  
    if type(data_json)==list: 
        try:
            for i in range(0,len(data_json)):
                data_send = np.array([value for value in data_json[i].values()])
                #print(i,type(data_send))
                
            #por cada elemento del json recibido creamos una fila en nuestra base de datos
                entries = entry(sepal_length=data_send[0],sepal_width=data_send[1],petal_length=data_send[2],petal_width=data_send[3],specie=data_send[4])
                
                db.session.add(entries)
                db.session.commit()
                result= "Added correctly",200
        except:
            result = "The model expecting 5 features as input",400
    else:
        result="Error input type: list required",400

    return result

@app.route('/train', methods=["POST"])
@jwt_required()
def train_model():
    file = request.files['']
    print("---------",file)
    result = train(file)

    return result


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)