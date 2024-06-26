# -*- coding: utf-8 -*-
"""RasLast.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RC9J8VUWpCrG9sVlE6OYZspX9KiOdafl
"""

import datetime
import numpy as np
import pandas as pd
from scipy.io import loadmat
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time
from sklearn.model_selection import KFold
import tensorflow as tf
from sklearn.metrics import r2_score

# Assuming your dataset loading and preprocessing remains the same
dataset = pd.read_csv("/home/senior/Downloads/BAT.csv").iloc[:,1:]

# Define attributes for preprocessing
attribs = ['cycle', 'voltage_measured', 'current_measured', 'temperature_measured', 'current_load', 'voltage_load']
train_dataset = dataset[attribs]

# Apply MinMaxScaler for normalization
sc = MinMaxScaler(feature_range=(0, 1))
train_dataset_normalized = sc.fit_transform(train_dataset)

# No need for reshaping into sequences since the model expects a sequence length of 1
input_data = train_dataset_normalized[-1:]  # Selecting the first sample for demonstration
input_data = np.nan_to_num(input_data)

TF_LITE_MODEL_FILE_NAME = '/home/senior/Downloads/tflite_model_float16.tflite'

interpreter = tf.lite.Interpreter(model_path=TF_LITE_MODEL_FILE_NAME)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

feature_dim = input_data.shape[1]
# Function to predict SoH for a given input data
def predict_soh(input_sample):
    # Ensure input data matches the model's expected input type
    input_sample_processed = input_sample.astype(input_details[0]['dtype'])

    # Run prediction
    interpreter.set_tensor(input_details[0]['index'], input_sample_processed)
    interpreter.invoke()

    # Extract the output
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data[0, 0]

# Select the last input for prediction
last_input_data = train_dataset_normalized[-1:].reshape(1, 1, feature_dim)
last_prediction = predict_soh(last_input_data)

# Handle outlier prediction
if last_prediction > 1:
    # If the last prediction is an outlier, take the last 4 inputs
    last_four_inputs = train_dataset_normalized[-4:].reshape(4, 1, feature_dim)
    predictions = [predict_soh(last_four_inputs[i].reshape(1, 1, feature_dim)) for i in range(4)]

    # Calculate the mean of the predictions
    corrected_prediction = np.mean(predictions)
    print(f'Original prediction was an outlier (SoH > 1). Corrected Prediction (mean of last 4 inputs): {corrected_prediction}')
else:
    print(f'Prediction for the last input: {last_prediction}')



