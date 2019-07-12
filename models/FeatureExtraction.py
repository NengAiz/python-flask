class FeatureExtraction:
    def __init__(self):
        self.__id = ""
        self.__median = ""
        self.__st_deviasi = ""
        self.__mean = ""

    def setId(self,id):
        self.__id = id

    def getId(self):
        return self.__id

    def setMedian(self,median):
    	self.__median = median

    def getMedian(self):
    	return self.__median

    def setStDeviasi(self,st_deviasi):
    	self.__st_deviasi = st_deviasi

    def getStDeviasi(self):
    	return self.__st_deviasi

    def setMean(self,mean):
    	self.__mean = mean

    def getMean(self):
    	return self.__mean