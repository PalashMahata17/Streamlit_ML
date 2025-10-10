import streamlit as st
import pandas as pd
import pickle
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Food Waste Predictor",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODEL LOADING ---
# Use a cache decorator to load the model only once
@st.cache_resource
def load_model():
    with open('food_waste_predictor.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

# --- SIDEBAR CONTENT ---
st.sidebar.title("About the App")
st.sidebar.info(
    "This application predicts food wastage at events to help businesses "
    "optimize food orders, reduce costs, and promote sustainability. "
    "It uses a trained XGBoost regression model."
)
st.sidebar.header("Created by Palash")

# --- MAIN PAGE CONTENT ---
st.title("🍽️ Food Waste Prediction Dashboard")
st.markdown("Predict food wastage with high accuracy and make smarter, more sustainable decisions.")

# --- INPUT SECTION ---
with st.container():
    st.header("Enter Event Details")
    
    # Create columns for a more organized layout
    col1, col2 = st.columns(2)

    with col1:
        num_guests = st.number_input("Number of Guests", min_value=1, value=100, step=10, help="Total expected attendees.")
        event_type = st.selectbox("Event Type", ['Corporate', 'Wedding', 'Birthday', 'Social Gathering'])
        seasonality = st.selectbox("Seasonality", ['Summer', 'Winter', 'Spring', 'Autumn', 'All Seasons'])
        
    with col2:
        quantity_food = st.number_input("Quantity of Food (in kg)", min_value=1.0, value=50.0, step=5.0, help="Total food prepared in kilograms.")
        type_of_food = st.selectbox("Type of Food", ['Meat', 'Vegetables', 'Dairy Products', 'Baked Goods', 'Fruits'])
        storage_conditions = st.selectbox("Storage Conditions", ['Refrigerated', 'Room Temperature', 'Frozen'])

# --- PREDICTION AND DISPLAY ---
if st.button("✨ Predict Wastage", type="primary"):
    if quantity_food > 0:
        # Create input DataFrame for the model
        input_data = {
            "Number of Guests": num_guests,
            "Quantity of Food": quantity_food,
            "waste_ratio": 0,  # This is a placeholder as it's part of the target logic
            "guests_per_food": num_guests / quantity_food,
            "Event Type": event_type,
            "Type of Food": type_of_food,
