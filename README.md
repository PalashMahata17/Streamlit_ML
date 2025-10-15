<img width="1337" height="934" alt="image" src="https://github.com/user-attachments/assets/e7120f63-8ae2-4621-8f7b-6189454de210" />

# Project Overview :

Food waste is a significant financial and environmental issue for the catering and hospitality industries. 
This project tackles this problem by providing a simple tool for event planners and caterers to accurately forecast the amount of food that will likely be wasted. 
By inputting key details about an event, users can get an instant prediction, enabling them to make data-driven decisions on food procurement.

# Key Features
1.Interactive UI:** A user-friendly interface built with Streamlit to input event parameters.

2.Real-time Predictions:** The app uses a trained **XGBoost Regressor** model to provide instant and accurate wastage predictions in kilograms.

3.Comprehensive Inputs:** Allows users to specify details like the number of guests, quantity of food, event type, seasonality, and more.

4.Data-Driven Insights:** Empowers businesses to reduce costs, minimize their environmental footprint, and operate more efficiently.

# Methodology & Tech Stack

1.Exploratory Data Analysis (EDA):** The initial dataset was analyzed to understand correlations and patterns between features like guest count, food quantity, and waste.

2.Feature Engineering:** New features such as `waste_ratio` and `guests_per_food` were created to improve model performance.

3.Model Comparison:** Several regression models were trained and evaluated, including Linear Regression, Decision Tree, Random Forest, and Gradient Boosting.

4.Final Model:** **XGBoost Regressor** was selected as the final model due to its superior performance, achieving an **R² of over 0.99** on the test set.

**Key Libraries Used:**
* `scikit-learn` for data preprocessing and modeling pipelines.
* `pandas` for data manipulation.
* `XGBoost` for the final regression model.
* `Streamlit` for building and deploying the interactive web app.
