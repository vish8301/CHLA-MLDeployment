import streamlit as st
import requests
import pandas as pd
import os

def main():
    st.markdown("""
    <style>
        .centered-text {
            text-align: center;
            font-size: 24px; /* or any other size */
            font-weight: bold; /* if you want it bold */
        }
    </style>
    <div class="centered-text">CHLA Resource</div>
    """, unsafe_allow_html=True)

    html_temp = """
    <div style="background:#22333b ;padding:10px">
    <h2 style="color:white;text-align:center;">Appointment No Show Prediction App </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    st.info("Please fill in the details of the appointment to predict if the patient will attend")

    # Load data
    df = pd.read_csv("CHLA_clean_data_2024_Appointments.csv")
    df['APPT_DATE'] = pd.to_datetime(df['APPT_DATE'], format='%m/%d/%y %H:%M')

    ### Date inputs
    col1, col2 = st.columns([1, 1])
    with col1:
        start_datetime = st.date_input("Start Date", min_value=df['APPT_DATE'].min(), max_value=df['APPT_DATE'].max())
    with col2:
        end_datetime = st.date_input("End Date", min_value=df['APPT_DATE'].min(), max_value=df['APPT_DATE'].max())

    if start_datetime and end_datetime:
        if start_datetime > end_datetime:
            st.error("End Date should be after Start Date")
        else:
            clinic_selector = st.multiselect("Select a Clinic", options=sorted(df['CLINIC'].unique()))

            if st.button("Predict"):
                if not clinic_selector:
                    st.error("Please select at least one clinic.")
                else:
                    # Backend API URL from Environment Variable
                    backend_url = os.getenv('BACKEND_URL', 'http://localhost:8000') + "/predict/"

                    # Send request to backend
                    response = requests.post(backend_url, json={
                        "start_date": str(start_datetime),
                        "end_date": str(end_datetime),
                        "clinics": clinic_selector
                    })

                    if response.status_code == 200:
                        results = response.json()
                        if results:
                            # Process results and display
                            results_df = pd.DataFrame(results)
                            results_df['APPT_DATE'] = pd.to_datetime(results_df['APPT_DATE'])
                            results_df['Date'] = results_df['APPT_DATE'].dt.date
                            results_df['Time'] = results_df['APPT_DATE'].dt.time
                            results_df['MRN'] = results_df['MRN'].astype(str)
                            results_df['APPT_ID'] = results_df['APPT_ID'].astype(str)
                            st.dataframe(results_df[['MRN', 'APPT_ID', 'Date', 'Time', 'CLINIC', 'NO SHOW (Y/N)', 'Probability']])
                        else:
                            st.error("No appointments found for the selected clinics in the given date range")
                    else:
                        st.error("Failed to retrieve predictions: " + response.text)
            else:
                st.error("Prediction button not pressed")
    else:
        st.warning("Please select both a start and end date")

if __name__ == '__main__':
    main()
