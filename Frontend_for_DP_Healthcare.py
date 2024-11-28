import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Simulate or load pricing and resource data
def generate_dummy_data():
    dates = [datetime.now() - timedelta(days=i) for i in range(30)]
    demand = np.random.randint(50, 200, size=30)
    capacity = np.random.randint(100, 300, size=30)
    prices = demand * 0.8 + capacity * 0.2 + np.random.randint(-10, 10, size=30)

    data = {
        "Date": dates,
        "Demand": demand,
        "Capacity": capacity,
        "Price": prices,
    }
    return pd.DataFrame(data)

# Load data
data = generate_dummy_data()

# Set up Streamlit interface
st.set_page_config(page_title="Healthcare Pricing Dashboard", layout="wide")
st.title("Healthcare Dynamic Pricing Dashboard")
st.markdown("Monitor pricing trends, demand, and resource utilization in real-time.")

# Display Key Metrics
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Price", f"${data['Price'].mean():.2f}")
col2.metric("Average Demand", f"{data['Demand'].mean():.0f} patients")
col3.metric("Average Capacity", f"{data['Capacity'].mean():.0f} slots")

# Pricing Trends Visualization
st.subheader("Pricing Trends")
price_fig = px.line(
    data,
    x="Date",
    y="Price",
    title="Daily Pricing Trends",
    labels={"Price": "Price ($)", "Date": "Date"},
)
st.plotly_chart(price_fig, use_container_width=True)

# Demand vs. Capacity Visualization
st.subheader("Demand vs. Capacity")
demand_capacity_fig = px.bar(
    data,
    x="Date",
    y=["Demand", "Capacity"],
    title="Demand and Capacity Over Time",
    labels={"value": "Count", "Date": "Date"},
    barmode="group",
)
st.plotly_chart(demand_capacity_fig, use_container_width=True)

# Upload New Data
st.subheader("Update Data")
uploaded_file = st.file_uploader("Upload new CSV file", type=["csv"])
if uploaded_file:
    new_data = pd.read_csv(uploaded_file)
    st.success("New data uploaded successfully!")
    st.write(new_data)

# Export Data
st.subheader("Export Data")
if st.button("Download Current Data"):
    data.to_csv("current_data.csv", index=False)
    st.success("Data exported successfully!")

# Resource Utilization Table
st.subheader("Resource Utilization Details")
st.dataframe(data[["Date", "Demand", "Capacity", "Price"]].style.format({"Price": "${:.2f}"}))
