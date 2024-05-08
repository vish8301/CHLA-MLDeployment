# CHLA no-show Prediction Model Deployment


**Streamlit App Link:** https://appointmentpredictiontool.streamlit.app/


## Overview
This repository contains the code and deployment setup for the CHLA Project - a machine learning model aimed at predicting patient no-shows at Children's Hospital Los Angeles (CHLA), deployed using Streamlit. The objective is to accurately predict whether a patient will show up for their scheduled appointment using historical CHLA data.

The complete project has the following parts (aimed to explore different methods of deployment):
- Project-01: Model Development and Deployment using Azure ML Studio (not in this repo).
- Project-02: Model Developed using python (sci-kit learn), Created and Deployed as Streamlit App.
- Project-03: Deployed Streamlit app using Docker (containerization).
- Project-04: Deployed Streamlit app using FastAPI (and also Docker for containerization).
- Project-05: Deployed Streamlit app using AWS (not in this repo).


## Dataset
The data used to train the model is proprietary and hence, cannot be shared. The `CHLA_clean_data_2024_Appointments.csv` file contains the data for scheduled patients on which the predictions are made.


## Model Development
A variety of machine learning algorithms and hyperparameters were explored to select the best-performing model. The Random Forest Classifier was chosen due to its robustness and performance across several metrics crucial to the no-show prediction problem. Emphasis was placed on recall, precision, F1-score, and ROC-AUC, given the high costs associated with false predictions. <br>
<br>
Models tested for Project 2-5 (for project-01, every 2 class algorithm available in Azure ML Studio was used): <br>
- Random Forest Classifier
- Gradient Boost Classifier
- AdaBoost Classifier


## Feature Selection
Top predictive features were carefully selected based on their impact on model performance, with a methodical approach involving correlation analysis, feature importance ranking, and domain knowledge. 


## Deployment
For Project-02, the final model was deployed using Streamlit in two different modes:
- Local Machine
- Github + Streamlit Server

For Project-03, the final model was deployed as a Docker Container on localhost.

For Project-04, components of the app were split: frontend & backend. The backend was deployed using FastAPI, and both the components were containerized using Docker.

For Project-05, the final model was deployed using AWS.


## Public URL
The model is deployed and publicly accessible at the following Streamlit Server URL: <br>
https://appointmentpredictiontool.streamlit.app/

## Repository Contents
- app.py - contains the code for the Streamlit deployed app.
- project2Final.ipynb - contains the code to explore the data, test the different models, and save the best final model.
- model.pkl - pickle file of the saved best model.
- encoder.pkl - pickle file of the encoded features from the notebook file.
- requirements.txt - the package requirements to deploy and run the model and app.

## Getting Started
To run the Streamlit app locally, clone the repository, install the dependencies, and execute the Streamlit run command:
```sh
git clone https://github.com/vish8301/MLDeployment.git
cd CHLA-MLDeployment
pip install -r requirements.txt
streamlit run app.py
