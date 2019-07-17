import pymysql.cursors
from models.Data import Data
from models.FeatureExtraction import FeatureExtraction

class Db:

	def getConnection():
	    return pymysql.connect(host='127.0.0.1',user='root',password='',db='tembakau',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)


	def insert_tembakau(nama,label,median,standarDeviasi,rataRata):
		conn = Db.getConnection()
		myCursor = conn.cursor()
		sql = "INSERT INTO tb_tembakau(nama,label,median,standarDevisiasi,rataRata) VALUES(%s,%s,%s,%s,%s)"
		val = (str(nama),str(label),str(median),str(standarDeviasi),str(rataRata))
		myCursor.execute(sql,val) 
		conn.commit()
		conn.close()

	def selectDataTembakau():
		conn = Db.getConnection()
		myCursor = conn.cursor()
		sql = 'SELECT * from tembakau_tb'
		myCursor.execute(sql) 
		result = myCursor.fetchall()
		conn.commit()
		conn.close()
		allData = []
		for x in range(0, len(result)):
			data = Data()
			data.setId(result[x]['id'])
			data.setName(result[x]['nama'])
			data.setLabel(result[x]['label'])
			data.setMedian(result[x]['median'])
			data.setStDeviasi(result[x]['standarDeviasi'])
			data.setR(result[x]['rataRata'])
			allData.append(data)
		return allData;
