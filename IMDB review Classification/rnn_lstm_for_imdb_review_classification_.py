# -*- coding: utf-8 -*-
"""RNN -LSTM for IMDB Review Classification - .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hgA_Kok2LHGiyv5z1e90BlCNz-wJurm4

# Step 1: Installation and Setup
"""

! pip install tensorflow

import tensorflow as tf

print(tf.__version__)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""# Step 2: Data Preprocessing"""

# importing the libraries
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences

# loading the dataset
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words= 20000)

x_train

# apply padding
x_train = pad_sequences(x_train, maxlen=100)
x_test = pad_sequences(x_test, maxlen= 100)

x_train.shape, x_test.shape

"""# Step 3: Building the model"""

# Define an object (initilizing RNN)

model = tf.keras.models.Sequential()

# Embedding layer
model.add(tf.keras.layers.Embedding(input_dim=20000, output_dim= 128, input_shape=(100,)))

# LSTM layer
model.add(tf.keras.layers.LSTM(units=128, activation ='tanh'))

# Output layer
model.add(tf.keras.layers.Dense(units=1, activation ='sigmoid'))

model.summary()

# compile the model
model.compile(optimizer='rmsprop', loss ='binary_crossentropy', metrics = ['accuracy'])

"""# Step 4: Training the model"""

history = model.fit(x_train, y_train, batch_size=128, epochs = 5, validation_data= (x_test,y_test))

# predictions
y_pred_prob = model.predict(x_test)

# Apply threshold to convert probabilities to class labels (0 or 1)
y_pred = (y_pred_prob > 0.5).astype("int32")

print(y_pred[0]), print(y_test[0])

# confusion matrix
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)

acc_cm = accuracy_score(y_test, y_pred)
print(acc_cm)

"""# Step 5: Learning Curve"""

def learning_curve(history, epoch):

  # training vs validation accuracy
  epoch_range = range(1, epoch+1)
  plt.plot(epoch_range, history.history['accuracy'])
  plt.plot(epoch_range, history.history['val_accuracy'])
  plt.title('Model Accuracy')
  plt.ylabel('Accuracy')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'val'], loc='upper left')
  plt.show()

  # training vs validation loss
  plt.plot(epoch_range, history.history['loss'])
  plt.plot(epoch_range, history.history['val_loss'])
  plt.title('Model loss')
  plt.ylabel('loss')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'val'], loc='upper left')
  plt.show()

learning_curve(history, 5)

