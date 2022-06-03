from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
import sklearn
import time
import pymongo
import pandas as pd
from pymongo import MongoClient
import pickle
from sklearn.model_selection import train_test_split
from custom_logger import CustomLogger

app = Flask(__name__) # initializing a flask app

log = CustomLogger.log("mongo.log")

import sklearn
app = Flask(__name__)

model=pickle.load(open('finalized_model_extra_tree_regressor.pkl','rb'))


@app.route('/', methods=['GET'])
def home():
    return render_template("play.html")

@app.route('/regression', methods=['GET'])
def hello_world():
    return render_template("forest_fire.html")


@app.route('/predict_reg',methods=['POST','GET'])
@cross_origin()
def predict():
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(int_features)
    print(final)
    prediction=model.predict(final)
    output=prediction

    if str(output)>str(0.5):
        return render_template('forest_fire.html',pred='Your Forest is in Danger.\nProbability of temperature is {}'.format(output),bhai="kuch karna hain iska ab?")
    else:
        return render_template('forest_fire.html',pred='Your Forest is safe.\n Probability of temperature is {}'.format(output),bhai="Your Forest is Safe for now")




## Classification module


@app.route('/classification',methods=['GET', 'POST'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict_class',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            day = float(request.form['day'])
            month = float(request.form['month'])
            Temperature = float(request.form['Temperature'])
            RH = float(request.form['RH'])
            Ws = float(request.form['Ws'])
            Rain = float(request.form['Rain'])
            FFMC = float(request.form['FFMC'])
            DMC = float(request.form['DMC'])
            FWI = float(request.form['FWI'])

            filename = 'finalized_model_decision_tree.pkl'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            prediction = loaded_model.predict([[day, month, Temperature, RH, Ws, Rain, FFMC, DMC, FWI]])
            print('prediction is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=prediction)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')




### using MongoDB




@app.route('/mongodb', methods=['GET'])
def hello1_world():
    #return render_template("forest_fire.html")
    return render_template("mongodata.html")




@app.route('/predict_mongo',methods=['POST','GET'])
@cross_origin()
def prediction():
    # point the client at mongo URI
    client = pymongo.MongoClient(
        "mongodb+srv://mongodb:mongodb@cluster0.kacpywk.mongodb.net/?retryWrites=true&w=majority")

    collection = "features"
    MONGO_DB = "mydatabase"

    model_file = 'finalized_model_extra_tree_regressor.pkl'

    # select database
    db = client['mydatabase']
    # select the collection within the database
    test = db.features
    # convert entire collection to Pandas dataframe
    test = pd.DataFrame(list(test.find()))

    # saving the data loaded from the mongodb and removing first column
    df = test.drop(labels="_id", axis=1)

    ## Divide the data into x and y
    X = df[['day', 'month', 'RH', 'Ws', 'Rain', 'FFMC', 'DMC', 'FWI', 'Classes']]
    y = df['Temperature']

    ## split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # load the saved model
    # load the model from disk
    # with open('finalized_model_extra_tree_regressor.pkl' , 'rb') as f:
    #    et = pickle.load(f)

    ## predicting the values
    file_name = 'finalized_model_extra_tree_regressor.pkl'
    loaded_model = pickle.load(open(file_name, 'rb'))
    # predictions using the loaded model file

    try:
        prediction = loaded_model.predict(X_test)
        print('prediction is', prediction)
        # showing the prediction results in a UI
        return render_template('mongodata.html', prediction=prediction)

    except Exception as e:
     print('The Exception message is: ', e)
     return 'something is wrong'
    # return render_template('results.html')
    else:
     return render_template('index.html')







if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app


