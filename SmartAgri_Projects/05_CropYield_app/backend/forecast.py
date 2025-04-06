import pandas as pd
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import math

def haversine_distance(lon1, lat1, lon2, lat2):
    """Calculate the Haversine distance between two points on the earth."""
    R = 6371.0  # Earth radius in kilometers

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (math.sin(d_lat / 2) * math.sin(d_lat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) * math.sin(d_lon / 2))

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

def nearest_point(points_long, points_lat, test_point):
    """Find the nearest point from a list of points to a test point."""
    min_distance = float('inf')
    nearest = None

    for point in zip(points_long, points_lat):
        distance = haversine_distance(point[0], point[1], test_point[0], test_point[1])
        if distance < min_distance:
            min_distance = distance
            nearest = point

    return nearest

cleaned_df = pd.read_csv('crop_predicitve_analysis/Cleaned_yield_data.csv')

def transform_series(series, window_size):
    X, Y = [], []
    for i in range(len(series) - window_size):
        X.append(series[i:i+window_size])
        Y.append(series[i+window_size])
    return np.array(X), np.array(Y)

def predict_next_value(data, window_size=3, epochs=200):
    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_normalized = scaler.fit_transform(np.array(data).reshape(-1, 1))

    # Transform the data into a supervised learning problem
    X, Y = transform_series(data_normalized, window_size)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    # Define the LSTM model
    model = keras.Sequential([
        keras.layers.LSTM(50, activation='relu', input_shape=(window_size, 1)),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')

    # Train the model
    model.fit(X, Y, epochs=epochs, verbose=0)  # verbose=0 to suppress the training output

    # Predict the next value
    input_sequence = np.array(data_normalized[-window_size:]).reshape(1, window_size, 1)
    predicted_normalized = model.predict(input_sequence)

    # Denormalize the predicted value
    predicted_value = scaler.inverse_transform(predicted_normalized)

    return predicted_value[0][0]

def get_forecast(crop, long, lat, df = cleaned_df):
  df_req_crop = df[df['CROP'] == crop]

  nearest_cord = nearest_point(df_req_crop['LONGITUDE'], df_req_crop['LATITUDE'],(long, lat))

  df_req = df_req_crop[(df_req_crop['LONGITUDE'] == nearest_cord[0]) & (df_req_crop['LATITUDE'] == nearest_cord[1])]
  required_values = list(df_req.iloc[0,3:-2])
  next_val = predict_next_value(required_values)

  extended_data = required_values+[next_val]


  # Create time axis (for x-axis)
  time_axis = np.array(range(len(extended_data)))+1987
  time_axis = time_axis.astype(int)
  extended_data = [int(x) for x in extended_data]


  return time_axis,extended_data