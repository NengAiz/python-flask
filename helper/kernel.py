import numpy as np
import cv2

class kernel:
    
    def degree(x):
        return (x*(np.pi/180))
    
    def frequency_to_lamda(x):
        return (1/x)
    
    def getKernelTembakau():
        filters = []
        ksize = 49 
        scale  = [kernel.frequency_to_lamda(10),kernel.frequency_to_lamda(13),kernel.frequency_to_lamda(15),kernel.frequency_to_lamda(18),kernel.frequency_to_lamda(20),kernel.frequency_to_lamda(21),kernel.frequency_to_lamda(23),kernel.frequency_to_lamda(24)]
        theta = [kernel.degree(0),kernel.degree(30),kernel.degree(45),kernel.degree(57),kernel.degree(60),kernel.degree(90),kernel.degree(115),kernel.degree(120),kernel.degree(135),kernel.degree(150),kernel.degree(160),kernel.degree(175)]
        for i in np.arange(0, len(theta),1):
            for j in np.arange(0,len(scale),1):
                kern = cv2.getGaborKernel((ksize, ksize), 3.0,theta[i], scale[j], 0.5, 0, ktype=cv2.CV_32F)
                
                kern /= 1.5*kern.sum()
                filters.append(kern)
        return filters
    
 

#     def getKernelGabor(imgs, img):
#         filters = []
#         ksize = 49 
#         scale  = [kernel.frequency_to_lamda(10),kernel.frequency_to_lamda(13),kernel.frequency_to_lamda(15),kernel.frequency_to_lamda(18),kernel.frequency_to_lamda(20),kernel.frequency_to_lamda(21),kernel.frequency_to_lamda(23),kernel.frequency_to_lamda(24)]
#         theta = [kernel.degree(0),kernel.degree(30),kernel.degree(45),kernel.degree(57),kernel.degree(60),kernel.degree(90),kernel.degree(115),kernel.degree(120),kernel.degree(135),kernel.degree(150),kernel.degree(160),kernel.degree(175)]
#         for i in np.arange(0, len(theta),1):
#             for j in np.arange(0,len(scale),1):
#                 kern = cv2.getGaborKernel((ksize, ksize), 3.0,theta[i], scale[j], 0.5, 0, ktype=cv2.CV_32F)
#                 #normalisasi
#                 kern /= 1.5*kern.sum()
#                 # gabor filter
#                 gabor = kernel.gaborFiltering(img, kern)
#                 # extract features
#                 mean = kernel.getMean(gabor)
#                 median = kernel.getMedian(gabor)
#                 std = kernel.getSDeviate(gabor)
#                 # nama gambar, theta (degree), scale (freq), mean, median, std
#                 print([imgs, theta[i], scale[j], mean, median, std])
#                 filters.append([imgs, theta[i], scale[j], mean, median, std])
#         return filters
    
    def gaborFiltering(img, filters):
        all_accum=[]
        for i,kern in enumerate(filters):
            accum = np.zeros_like(img)
            fimg = cv2.filter2D(img, cv2.CV_16UC3, kern)
            np.maximum(accum, fimg, accum)
            #cv2.imshow('filter'+str(i), accum)
            all_accum.append(accum)
        return all_accum
    
    def getMean(var):
        jumlah = np.mean(var)
        print("mean = "+str(jumlah))
        return jumlah
    
    def getSDeviate(var):
        hasil = np.std(var)
        print("sdeviasi = "+str(hasil))
        return hasil
    
    def getMedian(var):
        hasil = np.median(var)
        print("median = "+str(hasil))
        return hasil