# Deploying ML API using Flask
Project to deploy a Machine Learnign model using Flask API

This project is an API created in flask that allows training and inference tasks of a predictive Machine Learning model.

## API Endpoints 

METHOD POST

/token 
Authentication the user and return a JWT token

/train 
Train the model with a provide file. Must send a csv file

/add_entry
Adds one or more entries to the database 

/predict 
Make predictions using a trained model


METHOD GET

/user
Show information about the authenticated user

## DATABASE  
Sqlite /pip install db-sqlite3/

## Project Structure

1. app.py - This contains Flas APIs
2. model.py - Machine Learning model
3. db.py - Database configuration 
4. model_db.py - Create database tables

## Running the project

From the terminal navigate to the project root folder. Run the following command to install all the 
necessary pip packages to run the program
```
    pip install -r requirements.txt
```
1. Run app.py using command to start Flask API
   ```
   python app.py
  
By default, flask will run on port 5000.

To predict it is necessary:
1. Generate a token with the allowed user:
localhost:5000/token

2. Train the model with a csv file:
localhost:5000/token

After training the model we are able to predict

