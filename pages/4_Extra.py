import streamlit as st
import pandas as pd

st.title("Extra Analytics & Statistics")
st.markdown("Here you can find a quick summary of key data extracted from the dataset.")

@st.cache_data
def load_data():
    # Load the dataset using a relative path
    file_path = "reservoirs.csv"
    df = pd.read_csv(file_path)
    
    # Clean potential invisible spaces around column names
    df.columns = df.columns.str.strip()
    
    # Rename columns to English
    df = df.rename(columns={
        'dato_Id': 'Date',
        'omrType': 'Area_Type',
        'omrnr': 'Area_Code',
        'iso_aar': 'Year',
        'iso_uke': 'Week',
        'fyllingsgrad': 'Fill_Rate',
        'kapasitet_TWh': 'Capacity_TWh',
        'fylling_TWh': 'Filling_TWh',
        'neste_Publiseringsdato': 'Next_Publish_Date'
    })
    return df

# Load the dataframe
df = load_data()

# Display the metrics in two layout columns
col1, col2 = st.columns(2)

with col1:
    # Display the average capacity
    st.metric("Average Total Capacity", f"{df['Capacity_TWh'].mean():.2f} TWh")

with col2:
    # Display the average fill rate converted to a percentage
    st.metric("Average Fill Rate", f"{df['Fill_Rate'].mean()*100:.1f}%")

# Display final success message
st.success("All project pages have been successfully configured!")