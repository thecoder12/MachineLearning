#!/usr/bin/env python
# coding: utf-8

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle
import numpy as np
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import TensorBoard
import time

NAME = 'Cats-vs-dogs-cnn-64x2-{}'.format(int(time.time()))
# print(tensorboard)

gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.333)
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))


X = pickle.load(open("X.pickle", "rb"))
y = pickle.load(open("y.pickle", "rb"))
y = np.array(y)

X = X/255.0


dense_layers = [0]
layer_sizes = [64]
conv_layers = [3]

for dense_layer in dense_layers:
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            NAME = "{}-conv-{}-nodes-{}-dense-{}".format(conv_layer, layer_size, dense_layer, int(time.time()))
            tensorboard = TensorBoard(log_dir='/Users/rohitkhandale/opt/anaconda3/envs/tensorflow_env/logs/{}'.format(NAME))
            print(NAME)

            model = Sequential()
            model.add(Conv2D(64,(3,3),input_shape = X.shape[1:]))  ##???
            model.add(Activation("relu")) ##??
            model.add(MaxPooling2D(pool_size=(2,2)))
            
            for l in range(conv_layer-1):
                model.add(Conv2D(64,(3,3)))  ##???
                model.add(Activation("relu")) ##??
                model.add(MaxPooling2D(pool_size=(2,2)))

            model.add(Flatten())
            
            for l in range(dense_layer):
                model.add(Dense(512))
                model.add(Activation("relu"))
                model.add(Dropot(0.2))
#             model.add(Activation("relu"))


            model.add(Dense(1))
            model.add(Activation("sigmoid"))

            model.compile(loss="binary_crossentropy",
                         optimizer="adam",
                         metrics=["accuracy"])

            model.fit(X,y, batch_size=32, epochs=10, validation_split=0.3, callbacks=[tensorboard])

model.save('64x3-CNN.model')
