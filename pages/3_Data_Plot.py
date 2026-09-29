import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Reservoir chart")
st.markdown("Visualizing the fill level trend over time")

@st.cache_data
def load_data():
    # Load the dataset using a relative path
    df = pd.read_csv("reservoirs.csv")
    
    # Clean invisible spaces from column names
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
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Group by date to get a clean average and remove daily duplicates
    df_trend = df.groupby('Date')[['Fill_Rate', 'Capacity_TWh', 'Filling_TWh']].mean().reset_index()
    
    # Create a specific column in "YYYY-MM" format for the monthly slider
    df_trend['Month_Year'] = df_trend['Date'].dt.strftime('%Y-%m')
    
    return df_trend

df = load_data()

# 1. Here I create a dropdown menu with an "All" option to choose which metric to display
metric_options = ["All", "Fill_Rate", "Capacity_TWh", "Filling_TWh"]
selected_metric = st.selectbox("Select the metric to analyze:", options=metric_options)

# 2. Time slider based on months
unique_months = df['Month_Year'].sort_values().unique()

# Set the default value to the first month (unique_months[0]) for both ends
selected_months = st.select_slider(
    "Select the month range:",
    options=unique_months,
    value=(unique_months[0], unique_months[0])
)

# Filter data based on the slider selection
start_month, end_month = selected_months
filtered_df = df[(df['Month_Year'] >= start_month) & (df['Month_Year'] <= end_month)]

st.subheader(f"Trend for {selected_metric}")

# 3. Create the chart with Matplotlib to handle axis titles and different scales
fig, ax = plt.subplots(figsize=(10, 5))

if selected_metric == "All":
    # Min-Max normalization to plot metrics with different scales (TWh and percentages)
    for col in ["Fill_Rate", "Capacity_TWh", "Filling_TWh"]:
        min_val = filtered_df[col].min()
        max_val = filtered_df[col].max()
        
        # Avoid division by zero if the value is constant during the selected period
        if min_val != max_val:
            normalized_col = (filtered_df[col] - min_val) / (max_val - min_val)
        else:
            normalized_col = pd.Series(1.0, index=filtered_df.index)
            
        ax.plot(filtered_df['Date'], normalized_col, label=f"Normalized {col}")
    
    # Force Y-axis to stay between 0 and 1 with a small margin
    ax.set_ylim(-0.1, 1.1)
    ax.set_ylabel("Normalized Scale (0-1)")
else:
    # Plot the single selected metric
    ax.plot(filtered_df['Date'], filtered_df[selected_metric], label=selected_metric, color='#1f77b4')
    ax.set_ylabel(selected_metric)

# Add formatting, titles, and grid as requested
ax.set_title("Reservoirs Trend Over Time")
ax.set_xlabel("Date")
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

# Render the chart in the Streamlit interface
st.pyplot(fig)