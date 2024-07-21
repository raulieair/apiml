import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np

import mlflow
import mlflow.sklearn

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

    except Exception as err:
        
        mlflow.log_params({"error": str(err)})
    except Warning as warn:
        
        mlflow.log_params({"warning": str(warn)})
    finally:
        
        mlflow.end_run()

    
  
    return accuracy

