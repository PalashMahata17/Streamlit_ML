import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load the trained model
model = joblib.load('food_wastage_model.pkl')

# Define the Streamlit app title and layout
st.title('Food Wastage Prediction App')
st.write('Enter the details below to predict the food wastage amount.')

# Create input fields for features
number_of_guests = st.number_input('Number of Guests', min_value=1, value=250)
quantity_of_food = st.number_input('Quantity of Food', min_value=1, value=350)
event_type = st.selectbox('Event Type', ['Corporate', 'Birthday', 'Social Gathering', 'Wedding'])
type_of_food = st.selectbox('Type of Food', ['Meat', 'Vegetables', 'Baked Goods', 'Dairy Products', 'Fruits'])
storage_conditions = st.selectbox('Storage Conditions', ['Refrigerated', 'Room Temperature'])
seasonality = st.selectbox('Seasonality', ['Winter', 'Summer', 'All Seasons'])

# Calculate engineered features
waste_ratio = st.slider('Waste Ratio (Manual Input for Sensitivity)', 0.0, 1.0, 0.05) # Allow manual input for demonstration
guests_per_food = number_of_guests / quantity_of_food if quantity_of_food > 0 else 0


# Prepare input data for prediction
def prepare_input_df(guests, quantity, event, food_type, storage, season, waste_ratio_input, guests_per_food_input):
    # Create a dictionary with the input data
    data = {
        'Number of Guests': [guests],
        'Quantity of Food': [quantity],
        'waste_ratio': [waste_ratio_input],
        'guests_per_food': [guests_per_food_input],
        'Event Type': [event],
        'Type of Food': [food_type],
        'Storage Conditions': [storage],
        'Seasonality': [season]
    }
    input_df = pd.DataFrame(data)

    # Apply one-hot encoding - ensure all possible columns from training are present
    event_types = ['Corporate', 'Birthday', 'Social Gathering', 'Wedding']
    food_types = ['Meat', 'Vegetables', 'Baked Goods', 'Dairy Products', 'Fruits']
    storage_conditions_types = ['Refrigerated', 'Room Temperature']
    seasonality_types = ['Winter', 'Summer', 'All Seasons']

    for et in event_types:
        input_df[f'Event Type_{et}'] = (input_df['Event Type'] == et).astype(int)
    for ft in food_types:
        input_df[f'Type of Food_{ft}'] = (input_df['Type of Food'] == ft).astype(int)
    for st_cond in storage_conditions_types:
         input_df[f'Storage Conditions_{st_cond}'] = (input_df['Storage Conditions'] == st_cond).astype(int)
    for ssn in seasonality_types:
         input_df[f'Seasonality_{ssn}'] = (input_df['Seasonality'] == ssn).astype(int)


    # Drop original categorical columns
    input_df = input_df.drop(columns=['Event Type', 'Type of Food', 'Storage Conditions', 'Seasonality'])

    # Ensure column order and presence match training data (based on X_train columns)
    # Note: This assumes you have access to the columns of the training data X_train
    # For a real deployment, you would save the column list during training
    # For this example, we'll manually define the expected columns based on the training history
    expected_columns = [
        'Number of Guests', 'Quantity of Food', 'waste_ratio', 'guests_per_food',
        'Event Type_Corporate', 'Event Type_Social Gathering', 'Event Type_Wedding',
        'Type of Food_Dairy Products', 'Type of Food_Fruits', 'Type of Food_Meat', 'Type of Food_Vegetables',
        'Storage Conditions_Room Temperature',
        'Seasonality_Summer', 'Seasonality_Winter'
    ]

    # Add missing columns with 0 and reorder
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[expected_columns]

    return input_df

# Prediction button
if st.button('Predict Wastage'):
    input_df = prepare_input_df(
        number_of_guests,
        quantity_of_food,
        event_type,
        type_of_food,
        storage_conditions,
        seasonality,
        waste_ratio,
        guests_per_food
    )
    prediction = model.predict(input_df)
    st.success(f'Predicted Food Wastage Amount: {prediction[0]:.2f}')
