from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import numpy as np
from typing import List  # Import List from typing

app = FastAPI()

# Load data
df = pd.read_csv("CHLA_clean_data_2024_Appointments.csv")
df['APPT_DATE'] = pd.to_datetime(df['APPT_DATE'], format='%m/%d/%y %H:%M')

# Load model and encoder
model = pickle.load(open('model.pkl', 'rb'))
le = LabelEncoder()
le.fit(df['CLINIC'].unique())  # Assuming 'CLINIC' needs to be encoded

class AppointmentQuery(BaseModel):
    start_date: str
    end_date: str
    clinics: List[str]  # Use List from typing module

@app.post("/predict/")
def predict(query: AppointmentQuery):
    start_datetime = pd.to_datetime(query.start_date)
    end_datetime = pd.to_datetime(query.end_date)

    # Filter data
    mask = (df['APPT_DATE'] >= start_datetime) & (df['APPT_DATE'] <= end_datetime)
    filtered_df = df[mask]
    if not filtered_df.empty:
        filtered_df = filtered_df[filtered_df['CLINIC'].isin(query.clinics)]

    if filtered_df.empty:
        raise HTTPException(status_code=404, detail="No data available for the selected criteria.")

    # Prepare data for prediction
    pdf = filtered_df[['AGE', 'CLINIC', 'TOTAL_NUMBER_OF_CANCELLATIONS', 'LEAD_TIME',
                       'TOTAL_NUMBER_OF_RESCHEDULED', 'TOTAL_NUMBER_OF_NOSHOW',
                       'TOTAL_NUMBER_OF_SUCCESS_APPOINTMENT', 'HOUR_OF_DAY', 'NUM_OF_MONTH']]
    pdf['CLINIC'] = le.transform(pdf['CLINIC'])

    # Make predictions
    predictions = model.predict(pdf)
    probabilities = model.predict_proba(pdf)[:, 1]  # Probability of 'YES'
    
    # Add predictions to dataframe
    filtered_df['NO SHOW (Y/N)'] = ['YES' if x == 1 else 'NO' for x in predictions]
    filtered_df['Probability'] = probabilities

    # Selecting and returning relevant columns
    result = filtered_df[['MRN', 'APPT_ID', 'APPT_DATE', 'CLINIC', 'NO SHOW (Y/N)', 'Probability']]
    return result.to_dict(orient='records')
