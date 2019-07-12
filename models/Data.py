class Data:
    def __init__(self):
        self.__id = ""
        self.__nama = ""
        self.__label = ""
        self.__median = ""
        self.__standarDeviasi = ""
        self.__rataRata = ""

    def setId(self,id):
        self.__id = id

    def getId(self):
        return self.__id

    def setName(self,nama):
        self.__nama = nama

    def getName(self):
        return self.__nama

    def setLabel(self,label):
        self.label = label

    def getLabel(self):
        return self.label
    
    def setMedian(self,median):
        self.__median = median

    def getMedian(self):
        return self.__median

    def setStDeviasi(self,standarDeviasi):
        self.__standarDeviasi = standarDeviasi

    def getStDeviasi(self):
        return self.__standarDeviasi


    def setR(self,rataRata):
        self.__rataRata = rataRata

    def getR(self):
        return self.__rataRata