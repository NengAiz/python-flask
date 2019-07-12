#!flask/bin/python
# from flask import Flask
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from skimage import io
from os import listdir

import numpy as np
import cv2
import csv

from connection.Db import Db
from models import Data

import pandas as pd


from helper.kernel import kernel
import pandas as pd

from flask import Flask, jsonify


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
    
# def getImage():
#     if request.method == 'POST':
#     	file = request.form
#         imageData = file['image']
#         imageName = file['name']
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO images(image, name) VALUES (%s, %s)", (imageData, imageName))
#         if(mysqli_query($conn, $insertSQL)){
#             file_put_contents($ImagePath,base64_decode($ImageData));
#             echo "Your Image Has Been Uploaded.";
#         }
#         mysql.connection.commit()
#         cur.close()

#         return 'success'
#         file = request.files['pic']
#         filename = file.filename
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         processImage(filename)            
#     else:
#         return "Y U NO USE POST?"
    
def trainData():
	train0 = Db.selectData(0)
	train1 = Db.selectData(1)
	train2 = Db.selectData(2)

	train = train0 + train1 + train2

	dataTrain = []
	for datum in train:    
	    dataTrain.append([datum.getStDeviasi(),datum.getR(),datum.getMedian(),datum.getLabel()])
	    
	# Creating a dataframe object from listoftuples
	dataTrain_df = pd.DataFrame(dataTrain,columns=["st_dev", "r", "median","label"]) 
	# print(dataTrain_df)
	trainX = dataTrain_df[["st_dev","r","median"]]
	trainY = dataTrain_df["label"]

	#---------------------------------------------------------------------------
	dataTest = []
	for datum in train:    
	    dataTest.append([0.915908,  0.961283,  0.755319, -1])
	    
	# Creating a dataframe object from listoftuples
	dataTest_df = pd.DataFrame(dataTest,columns=["st_dev", "r", "median","label"]) 
	testX = dataTest_df[["st_dev","r","median"]]
	testY = dataTest_df["label"]

	from sklearn.neighbors import KNeighborsClassifier

	# Create KNN classifier
	knn3 = KNeighborsClassifier(n_neighbors = 5)

	# Fit the classifier to the data
	knn3.fit(trainX,trainY)

		# save model
	import pickle
	 
	# pickle list object
	 
	list_pickle_path = 'tembakau_data.pkl'
	 
	# Create an variable to pickle and open it in write mode
	list_pickle = open(list_pickle_path, 'wb')
	pickle.dump(knn3, list_pickle)
	list_pickle.close()

	# load model
	# unpickling the list object
	# Need to open the pickled list object into read mode
	list_unpickle = open(list_pickle_path, 'rb')
	 
	# load the unpickle object into a variable
	knn3 = pickle.load(list_unpickle)

	#show first 5 model predictions on the test data
	predictiongg = knn3.predict(testX)
	# print(2)
	print(predictiongg[0])
	print("hasil prediksi : {}".format(predictiongg[0]))
	return render_template('index.html')

def TestDataFromAndroid():
	data = []

	path=[]

	path.append('new')

	mean = np.zeros((len(path),35))
	median = np.zeros((len(path),35))
	sDeviation = np.zeros((len(path),35))

	max_median = 0
	max_sDeviation = 0
	max_mean = 0

	    
	for y in range(0,len(path)): #jumlah kelas
	    size = len(listdir(path[y])) #jumlah gambar
	    for x in range(0,size):
	        imgs = io.imread(path[y] + '/' + '('+str(x+1)+').png')
	        img_path = path[y] + '/' + '('+str(x+1)+').png'
	        img_r = cv2.resize(imgs, (256, 256))
	        # imgs = cv2.imread(path[y]+'('+str(x+1)+').png',0)
	        filters = kernel.getKernel()
	        res1 = kernel.gaborFiltering(img_r, filters)
	        mean[y][x]=kernel.getMean(res1)
	        sDeviation[y][x]=kernel.getSDeviate(res1)
	        median[y][x]=kernel.getMedian(res1)
	        
	        if(max_mean < mean[y][x]):
	            max_mean = mean[y][x]
	        
	        if(max_sDeviation < sDeviation[y][x]):
	            max_sDeviation = sDeviation[y][x]
	        
	        if(max_median < median[y][x]):
	            max_median = median[y][x]
	            
	        mean[y][x] /= max_mean
	        median[y][x] /= max_median
	        sDeviation[y][x] /= max_sDeviation

	        data = [mean[y][x],median[y][x],sDeviation[y][x], -1]


	return data

def hitungHasil():
	train0 = Db.selectData(0)
	train1 = Db.selectData(1)
	train2 = Db.selectData(2)

	train = train0 + train1 + train2

	dataTrain = []
	for datum in train:    
	    dataTrain.append([datum.getStDeviasi(),datum.getR(),datum.getMedian(),datum.getLabel()])
	    
	# Creating a dataframe object from listoftuples
	dataTrain_df = pd.DataFrame(dataTrain,columns=["st_dev", "r", "median","label"]) 
	# print(dataTrain_df)
	trainX = dataTrain_df[["st_dev","r","median"]]
	trainY = dataTrain_df["label"]

	#---------------------------------------------------------------------------
	
	testFromAndroid = [] #data yang akan diterima dari android
	testFromAndroid = getDataFromAndroid()

	dataTest = []
	for datum in train:    
	    # dataTest.append([0.915908,  0.961283,  0.755319, -1])
	    dataTest.append(testFromAndroid)
	    
	# Creating a dataframe object from listoftuples
	dataTest_df = pd.DataFrame(dataTest,columns=["st_dev", "r", "median","label"]) 
	testX = dataTest_df[["st_dev","r","median"]]
	testY = dataTest_df["label"]

	from sklearn.neighbors import KNeighborsClassifier

	# Create KNN classifier
	knn3 = KNeighborsClassifier(n_neighbors = 5)

	# Fit the classifier to the data
	knn3.fit(trainX,trainY)

		# save model
	import pickle
	 
	# pickle list object
	 
	list_pickle_path = 'tembakau_data.pkl'
	 
	# Create an variable to pickle and open it in write mode
	list_pickle = open(list_pickle_path, 'wb')
	pickle.dump(knn3, list_pickle)
	list_pickle.close()

	# load model
	# unpickling the list object
	# Need to open the pickled list object into read mode
	list_unpickle = open(list_pickle_path, 'rb')
	 
	# load the unpickle object into a variable
	knn3 = pickle.load(list_unpickle)

	#show first 5 model predictions on the test data
	predictiongg = knn3.predict(testX)
	# print(2)
	print(predictiongg[0])
	print("hasil prediksi : {}".format(predictiongg[0]))

	return predictiongg[0]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_prediksi():
	hasil = hitungHasil()
	return jsonify({'tasks': hasil})

if __name__ == '__main__':
    app.run(debug=True)

    # if request.method == "POST":
    #     details = request.form
    #     firstName = details['fname']
    #     lastName = details['lname']
    #     cur = mysql.connection.cursor()
    #     cur.execute("INSERT INTO MyUser(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
    #     mysql.connection.commit()
    #     cur.close()
    #     return 'success'
    # return render_template('index.html');
    # return 'success'