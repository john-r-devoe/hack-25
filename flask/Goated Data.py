import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import requests
import googlemaps
import os
from dotenv import load_dotenv
import google.generativeai as genai
import openai

# Load dataset

businessData = pd.read_csv('hacklyticsData.csv')
# Check dataset structure

#ESTIMATED FOOT TRAFFIC SCORE CREATION SECTION

    def pointGeneratingFunction(E,P,N):
    # Select Features (X) and Target (y)
    X = businessData[[' Estimated Foot Traffic']]  # Replace with relevant feature names
    y = businessData['EFT Scores']  # Replace with the actual target column

    # Split dataset into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Create Decision Tree Model
    model = RandomForestClassifier(n_estimators=100, max_depth=5,random_state = 42)  # I LOVE RANDOM FOREST
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)

    # Evaluate performance
    #print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    #print(metrics.classification_report(y_test, y_pred))

    # SCORE CREATION STUFF
    new_data = np.array([[5.7]])  # Use var to store generated Estimated Foot Traffic
    predicted_score = model.predict(new_data)
    print("Predicted Matching Score EFT:", predicted_score)




    #POPULATION DENSITY SCORE CREATION SECTION

    # Select Features (X) and Target (y)
    X = businessData[['Population Density']]  # Replace with relevant feature names
    y = businessData['PD Scores']  # Replace with the actual target column

    # Split dataset into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create Decision Tree Model
    model = RandomForestClassifier(n_estimators=100, max_depth=5,random_state = 42)  # I LOVE RANDOM FOREST
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)

    # Evaluate performance
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print(metrics.classification_report(y_test, y_pred))

    # SCORE CREATION STUFF
    new_data = np.array([[3750]])  # Use var to store generated Estimated Foot Traffic
    predicted_score = model.predict(new_data)
    print("Predicted Matching Score:", predicted_score)

    #NEAREST COMPETITOR DISTANCE SCORE CREATION SECTION

    # Select Features (X) and Target (y)
    X = businessData[[' Nearest Competitor Distance']]  # Replace with relevant feature names
    y = businessData['NCD Scores']  # Replace with the actual target column

    # Split dataset into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create Decision Tree Model
    model = RandomForestClassifier(n_estimators=100, max_depth=5,random_state = 42)  # I LOVE RANDOM FOREST
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)

    # Evaluate performance
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print(metrics.classification_report(y_test, y_pred))

    # SCORE CREATION STUFF
    new_data = np.array([[12]])  # Use var to store generated Estimated Foot Traffic
    predicted_score = model.predict(new_data)
    print("Predicted Matching Score:", predicted_score)

inputs = [address,industry,preferences]




