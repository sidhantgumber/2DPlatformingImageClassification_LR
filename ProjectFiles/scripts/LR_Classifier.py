# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 18:48:01 2023

@author: gumbe
"""

import numpy as np 
#import glob
import cv2
import os
import pandas as pd
from skimage.filters import sobel
import pickle 

class classifier:
    
    def __init__(self, path):
        
        
        self.train_images = []
        self.imagePath = path
    
    def feature_extractor(self, dataset):
        x_train = dataset
        image_dataset = pd.DataFrame()
        for image in range(x_train.shape[0]):  #iterate through each file 
            #print(image)
            
            df = pd.DataFrame()  #Temporary data frame to capture information for each loop.
            #Reset dataframe to blank after each loop.
            
            input_img = x_train[image, :,:,:]
            img = input_img
        ################################################################
        #START ADDING DATA TO THE DATAFRAME
        #Add feature extractors, e.g. edge detection, smoothing, etc. 
                
             # FEATURE 1 - Pixel values
             
            #Add pixel values to the data frame
            pixel_values = img.reshape(-1)
            df['Pixel_Value'] = pixel_values   #Pixel value itself as a feature
            #df['Image_Name'] = image   #Capture image name as we read multiple images
            
            # FEATURE 2 - Bunch of Gabor filter responses
            
                    #Generate Gabor features
            num = 1  #To count numbers up in order to give Gabor features a lable in the data frame
            kernels = []
            for theta in range(2):   #Define number of thetas
                theta = theta / 4. * np.pi
                for sigma in (1, 3):  #Sigma with 1 and 3
                    lamda = np.pi/4
                    gamma = 0.5
                    gabor_label = 'Gabor' + str(num)  #Label Gabor columns as Gabor1, Gabor2, etc.
        #                print(gabor_label)
                    ksize=9
                    kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, 0, ktype=cv2.CV_32F)    
                    kernels.append(kernel)
                    #Now filter the image and add values to a new column 
                    fimg = cv2.filter2D(img, cv2.CV_8UC3, kernel)
                    filtered_img = fimg.reshape(-1)
                    df[gabor_label] = filtered_img  #Labels columns as Gabor1, Gabor2, etc.
                    print(gabor_label, ': theta=', theta, ': sigma=', sigma, ': lamda=', lamda, ': gamma=', gamma)
                    num += 1  #Increment for gabor column label
                    
             
            # FEATURE 3 Sobel
            edge_sobel = sobel(img)
            edge_sobel1 = edge_sobel.reshape(-1)
            df['Sobel'] = edge_sobel1
           
            #Add more filters as needed
            
            #Append features from current image to the dataset
            #image_dataset = image_dataset.append(df)
            image_dataset = pd.concat([image_dataset, df])
            
        return image_dataset
    
    def predict(self):
        SIZE = 128
        img = cv2.imread(self.imagePath, cv2.IMREAD_COLOR) #Reading color images
        print("Image path: ", self.imagePath)
        img = cv2.resize(img, (SIZE, SIZE)) #Resize images
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) #Optional step. Change BGR to RGB
        # self.train_images.append(img)
        if isinstance(self.train_images, list):
            self.train_images.append(img)
        elif isinstance(self.train_images, np.ndarray):
            self.train_images = np.append(self.train_images, [img], axis=0)
        else:
            # Handle the case where self.train_images is neither a list nor a NumPy array
            raise TypeError("self.train_images must be a list or numpy array")
        # self.train_images = pd.concat([self.train_images, img], ignore_index=False)
        self.train_images = np.array(self.train_images)
        self.train_images = self.train_images / 255.0
        img1 = self.train_images[0]        
        input_img = np.expand_dims(img1, axis=0) #Expand dims so the input is (num images, x, y, c)
        input_img_features= self.feature_extractor(input_img)
        input_img_features = np.expand_dims(input_img_features, axis=0)
        input_img_for_RF = np.reshape(input_img_features, (input_img.shape[0], -1))
        with open('logistic_regression', 'rb') as f:
            mp = pickle.load(f)
        pickle_prediction = mp.predict(input_img_for_RF)
        #pickle_prediction = int(pickle_prediction)
        if pickle_prediction == 0:
            return 'cat'
        else: return 'dog'
    



path = "C:/Users/gumbe/OneDrive/Documents/Project/archive/train/dogs/"


# Set the directory path where your images are stored


# Loop over all files in the directory
# for filename in os.listdir(path):
#     # Check if the file is an image (e.g., .jpg, .png, .jpeg)
#     if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#         # Construct the full file path
#         file_path = os.path.join(path, filename)
#
#         clf = classifier()
#         print(clf.predict(file_path))
        
        
        # Add your image processing code here




    