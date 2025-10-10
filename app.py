import streamlit as st
import pandas as pd
import pickle

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Food Waste Predictor",
    page_icon="🍽️",
    layout="wide"
)

# --- MODEL LOADING ---
@st.cache_resource
def load_model():
    # This function loads the trained model from the .pkl file
    with open('food_waste_predictor.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

# --- SIDEBAR ---
st.sidebar.title("About")
st.sidebar.info(
    "This app predicts food wastage at events to help businesses "
    "optimize food orders and promote sustainability. It uses a trained XGBoost model."
)
st.sidebar.header("Created by Palash")


# --- MAIN PAGE LAYOUT ---
st.title("🍽️ Food Waste Prediction Dashboard")
st.markdown("Use this tool to predict potential food waste based on event details.")

# --- INPUT WIDGETS ---
with st.container():
    st.header("Enter Event Details")

    # Create two columns for a cleaner layout
    col1, col2 = st.columns(2)

    with col1:
        num_guests = st.number_input("Number of Guests", min_value=1, value=100, step=10, help="Total expected attendees.")
        event_type = st.selectbox("Event Type", ['Corporate', 'Wedding', 'Birthday', 'Social Gathering'])
        seasonality = st.selectbox("Seasonality", ['Summer', 'Winter', 'Spring', 'Autumn', 'All Seasons'])
        preparation_method = st.selectbox("Preparation Method", ['Buffet', 'Sit-down Dinner', 'Finger Food'])
        pricing = st.selectbox("Pricing", ['High', 'Moderate', 'Low'])

    with col2:
        quantity_food = st.number_input("Quantity of Food (kg)", min_value=1.0, value=50.0, step=5.0, help="Total food prepared in kilograms.")
        type_of_food = st.selectbox("Type of Food", ['Meat', 'Vegetables', 'Dairy Products', 'Baked Goods', 'Fruits'])
        storage_conditions = st.selectbox("Storage Conditions", ['Refrigerated', 'Room Temperature', 'Frozen'])
        geo_location = st.selectbox("Geographical Location", ['Urban', 'Suburban', 'Rural'])
        purchase_history = st.selectbox("Purchase History", ['Regular', 'Occasional', 'New'])

# --- PREDICTION LOGIC ---
if st.button("✨ Predict Wastage", type="primary"):
    if quantity_food > 0:
        # Create a dictionary from user inputs
        input_data = {
            "Number of Guests": num_guests,
            "Quantity of Food": quantity_food,
            "waste_ratio": 0, # Placeholder feature
            "guests_per_food": num_guests / quantity_food,
            "Event Type": event_type,
            "Type of Food": type_of_food,
            "Storage Conditions": storage_conditions,
            "Seasonality": seasonality,
            "Preparation Method": preparation_method,
            "Geographical Location": geo_location,
            "Pricing": pricing,
            "Purchase History": purchase_history
        }

        # Convert to a DataFrame that matches the model's training format
        input_df = pd.DataFrame([input_data])

        # Make a prediction
        prediction = model.predict(input_df)[0]

        # Display the result
        st.subheader("Prediction Result")
        st.metric(label="Predicted Food Wastage", value=f"{prediction:.2f} kg")
        st.success("Prediction complete. Use this value to optimize your food orders.")

    else:
        st.error("Quantity of Food must be greater than zero.")
