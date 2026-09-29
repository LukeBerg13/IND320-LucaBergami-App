import streamlit as st
import pandas as pd

st.title("Interactive reservoir table")
st.markdown("This page displays the first month's trend for each imported metric.")

@st.cache_data
def load_and_clean_data():
    # Load the dataset using a relative path 
    df = pd.read_csv("reservoirs.csv")
    
    # I.ve uesed this command to clean invisible spaces from column names
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
    
    # Convert Date to datetime format for filtering
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_and_clean_data()

# 1. Isolate the first month of the dataset
first_month = df['Date'].min().to_period('M')
df_first_month = df[df['Date'].dt.to_period('M') == first_month]

# 2. Group by date to get a single daily average
daily_trend = df_first_month.groupby('Date')[['Fill_Rate', 'Capacity_TWh', 'Filling_TWh']].mean()

# 3. Create a new dataframe where each row represents a column from the original data
chart_data = pd.DataFrame({
    "Metric": ["Fill Rate", "Capacity (TWh)", "Filling (TWh)"],
    "First Month Trend": [
        daily_trend['Fill_Rate'].tolist(),
        daily_trend['Capacity_TWh'].tolist(),
        daily_trend['Filling_TWh'].tolist()
    ]
})

st.subheader("First Month Trend Overview")

# 4. Display using st.dataframe and column_config for the sparkline
st.dataframe(
    chart_data,
    column_config={
        "First Month Trend": st.column_config.LineChartColumn(
            "Trend (First Month Only)",
            width="medium"
        )
    },
    hide_index=True,
    use_container_width=True
)