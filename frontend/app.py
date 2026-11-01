import streamlit as st
import pandas as pd
import requests

# Load options fo dropdowns
import json
with open("options.json") as f:
    options = json.load(f)

with open("numLimits.json") as f:
    numLimits = json.load(f)

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Product Sales Forcaster")

# Input fields for product and store data
Product_Weight = st.number_input("Product Weight", 
                                 min_value=0.0,
                                 value=numLimits["Product_Weight"]["median"])
w = numLimits["Product_Weight"]
if Product_Weight < w["min"] or Product_Weight > w["max"]:
    st.warning(f"Weight is outside the training range ({w['min']}–{w['max']}). "
               "The prediction may be less reliable.")
    
Product_Sugar_Content = st.selectbox("Product Sugar Content", options["Product_Sugar_Content"])
Product_Allocated_Area = st.number_input("Product Allocated Area", 
                                 min_value=0.0,
                                 value=numLimits["Product_Allocated_Area"]["median"],
                                 max_value = 1.0,
                                 step=0.001,
                                 format="%.3f")
w = numLimits["Product_Allocated_Area"]
if Product_Allocated_Area < w["min"] or Product_Allocated_Area > w["max"]:
    st.warning(f"Product Allocated Area is outside the training range ({w['min']}–{w['max']}). "
               "The prediction may be less reliable.")
Product_Type = st.selectbox("Product Type", options["Product_Type"])
Product_MRP = st.number_input("Product MRP", 
                              min_value=0.0, 
                              value=numLimits["Product_MRP"]["median"])
w = numLimits["Product_MRP"]
if Product_MRP < w["min"] or Product_MRP > w["max"]:
    st.warning(f"Product MRP is outside the training range ({w['min']}–{w['max']}). "
               "The prediction may be less reliable.")
Store_Size = st.selectbox("Store Size", options["Store_Size"])
Store_Location_City_Type = st.selectbox("Store Location City Type", options["Store_Location_City_Type"])
Store_Type = st.selectbox("Store Type", options["Store_Type"])

product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_Type": Product_Type,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type
}

if st.button("Predict", type='primary'):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict",
                                 json=product_data,
                                 timeout=10)
        if response.status_code == 200:
            result = response.json()
            predicted_sales = result["Sales"]
            st.write(f"Predicted Product Store Sales Total: {predicted_sales:.2f}")
        else:
            st.error(f"The backend returned an error (status {response.status_code}).")
    except requests.exceptions.RequestException:
        st.error("Could not reach the prediction service. Please try again in a moment.")
