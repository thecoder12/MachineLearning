#!/usr/bin/env python
# coding: utf-8


import numpy as np
import os
import cv2
import matplotlib.pyplot as plt

DATADIR = '/Users/rohitkhandale/Downloads/kagglecatsanddogs_3367a/PetImages'
CATEGORIES = ["Dog","Cat"]


for category in CATEGORIES: 
    path = os.path.join(DATADIR, category)  # path for cat & dogs
    for img in os.listdir(path):
        img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE) # convert image to array 
        plt.imshow(img_array, cmap="gray")
        plt.show()
        break  # 
    break    


IMG_SIZE = 50

new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
plt.imshow(new_array, cmap='gray')
plt.show()


training_data = []

def create_training_data():
    for category in CATEGORIES: 
        path = os.path.join(DATADIR, category)  # path for cat & dogs
        class_num = CATEGORIES.index(category)  # get dog=0 & cat=1 for labels
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE) # convert image to array 
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array, class_num])
#                 print(len(training_data))
            except Exception as e:
#                 print(e)
                pass
#             break
            
create_training_data()
print(len(training_data))

import random

random.shuffle(training_data)

for sample in training_data[:10]:
    print(sample[1])


X = []
y = []

for features, label in training_data:
    X.append(features)
    y.append(label)
    

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1) ###  1=>grayscale, -1?, IMG_SIZE?
# X[0]


import pickle

pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()


pickle_out = open("y.pickle", "wb")
pickle.dump(y, pickle_out)
pickle_out.close()

pickle_in = open("X.pickle", "rb")
X = pickle.load(pickle_in)
            
X[0]





