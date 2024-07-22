import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
from flask import jsonify

import mlflow
import mlflow.sklearn

file = "IRIS.csv"
def train(file):
    mlflow.start_run()
    try:
        data = pd.read_csv(file)
        features = ['sepal_length','sepal_width','petal_length','petal_width']

        X = data[features]
        Y = data['species']

        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        classifier = DecisionTreeClassifier()
        classifier = classifier.fit(x_train,y_train)

        y_pred = classifier.predict(x_test)
        accuracy = metrics.accuracy_score(y_test, y_pred)
        
        mlflow.log_param("random_state",42)

        mlflow.log_metric("accuracy",accuracy)

        mlflow.sklearn.log_model(classifier, "decision_tree_model")

        result = jsonify({"Accuracy":accuracy}), 200

    except Exception as err:
        
        mlflow.log_params({"error": str(err)})
        result = "Check that the file is optimal for training the model. It should use the following csv structure :\nsepal_length,sepal_width,petal_length,petal_width,species\n5.1,3.5,1.4,0.2,Iris-setosa (Example)", 400

    finally:
        
        mlflow.end_run()

    
  
    return result

