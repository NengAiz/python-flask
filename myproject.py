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

@app.route("/todo-api/feature-extraction-tembakau",methods=['POST'])
def featureDetectionTembakau():
	app.logger.info(app.config['UPLOAD_FOLDER'])
	img = request.files['image']
	img_name = secure_filename(img.filename)
	create_new_folder(app.config['UPLOAD_FOLDER'])
	saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
	app.logger.info("saving {}".format(saved_path))
	img.save(saved_path)
	os.chmod(saved_path, 0o755)
	resize = cv2.resize(cv2.imread(saved_path),(512,512))
	cv2.imwrite(saved_path,resize)

	img = cv2.imread(saved_path)
	filters = kernel.getKernelTembakau()#119
	res1 = kernel.gaborFiltering(img, filters)
	mean = kernel.getMean(res1)/112.05
	stDev = kernel.getSDeviate(res1)/112.81
	median = kernel.getMedian(res1)/94

	#data training
	training=Db.selectDataTembakau()
	dataTrain = []
	for datum in training:    
	    dataTrain.append([datum.getStDeviasi(),datum.getMean(),datum.getMedian(),datum.getLabel()])
	dataTrain_df = pd.DataFrame(dataTrain,columns=["st_dev", "r", "median","label"]) 
	trainX = dataTrain_df[["st_dev","r","median"]]
	trainY = dataTrain_df["label"]
	#data testing
	dataTest = []
	dataTest.append([stDev,mean,median,-1])

	dataTest_df = pd.DataFrame(dataTest,columns=["st_dev", "r", "median","label"]) 
	testX = dataTest_df[["st_dev","r","median"]]
	testY = dataTest_df["label"]


	knn3 = KNeighborsClassifier(n_neighbors = 5)

	knn3.fit(trainX,trainY)
	list_pickle_path = 'tembakau_data.pkl'
	list_pickle = open(list_pickle_path, 'wb')
	pickle.dump(knn3, list_pickle)
	list_pickle.close()
	list_unpickle = open(list_pickle_path, 'rb')
	knn3 = pickle.load(list_unpickle)
	predicting = knn3.predict(testX)

	return jsonify(
		hasil_prediksi = predicting[0]
    )

if __name__ == '__main__':
    app.run(debug=True)