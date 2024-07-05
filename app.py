from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load('car_price_prediction_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # List of all features expected by the model
    expected_features = [
        'Kilometers_Driven', 'Mileage', 'Engine', 'Power', 'Age_of_car', 'Seats',
        'Location_Bangalore', 'Location_Chennai', 'Location_Coimbatore', 'Location_Delhi', 'Location_Hyderabad', 
        'Location_Jaipur', 'Location_Kochi', 'Location_Kolkata', 'Location_Mumbai', 'Location_Pune',
        'Fuel_Type_Diesel', 'Fuel_Type_Electric', 'Fuel_Type_LPG', 'Fuel_Type_Petrol',
        'Transmission_Manual', 'Owner_Type_Fourth & Above', 'Owner_Type_Second', 'Owner_Type_Third',
        'Brand_Audi', 'Brand_BMW', 'Brand_Bentley', 'Brand_Chevrolet', 'Brand_Datsun', 'Brand_Fiat', 
        'Brand_Force', 'Brand_Ford', 'Brand_Honda', 'Brand_Hyundai', 'Brand_Isuzu', 'Brand_Jaguar', 
        'Brand_Jeep', 'Brand_Lamborghini', 'Brand_Land Rover', 'Brand_Mahindra', 'Brand_Maruti', 
        'Brand_Mercedes-Benz', 'Brand_Mini Cooper', 'Brand_Mitsubishi', 'Brand_Nissan', 'Brand_Porsche', 
        'Brand_Renault', 'Brand_Skoda', 'Brand_Smart', 'Brand_Tata', 'Brand_Toyota', 'Brand_Volkswagen', 
        'Brand_Volvo', 'Class_of_Brand_Low_class'
    ]

    # Create a zero-filled dataframe with the expected columns
    input_data = pd.DataFrame(0, index=[0], columns=expected_features)

    # Populate the dataframe with the input data
    input_data['Kilometers_Driven'] = data['kilometersDriven']
    input_data['Mileage'] = data['mileage']
    input_data['Engine'] = data['engine']
    input_data['Power'] = data['power']
    input_data['Age_of_car'] = data['ageOfCar']
    input_data['Seats'] = data['seats']

    # Set the appropriate location column to 1
    location_column = f"Location_{data['location']}"
    if location_column in input_data.columns:
        input_data[location_column] = 1

    # Set the appropriate fuel type column to 1
    fuel_type_column = f"Fuel_Type_{data['fuelType']}"
    if fuel_type_column in input_data.columns:
        input_data[fuel_type_column] = 1

    # Set the appropriate transmission column to 1
    if data['transmission'] == 'Manual':
        input_data['Transmission_Manual'] = 1

    # Set the appropriate owner type column to 1
    owner_type_column = f"Owner_Type_{data['ownerType']}"
    if owner_type_column in input_data.columns:
        input_data[owner_type_column] = 1

    # Set the appropriate brand column to 1
    brand_column = f"Brand_{data['brand']}"
    if brand_column in input_data.columns:
        input_data[brand_column] = 1

    # Set the appropriate class of brand column to 1
    class_of_brand_column = f"Class_of_Brand_{data['classOfBrand']}"
    if class_of_brand_column in input_data.columns:
        input_data[class_of_brand_column] = 1

    # Perform prediction
    prediction = model.predict(input_data)
    
    return jsonify({'price': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
