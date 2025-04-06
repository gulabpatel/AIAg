from scripts.soil import get_data_JSON,loaded_model,chain1,chain2
import random
import json

with open('assets/sensor_data.json', 'r') as infile:
        sensor_data = json.load(infile)


def info_response(input_sensor):
        data_json = get_data_JSON(input_sensor, loaded_model)
        print(data_json)
        explanation = chain1.predict(data_JSON = data_json)
        return explanation
        

def chat_response_user(history, message):
        explanation = chain2.predict(user_history = history, user_message = message)
        return explanation

def get_sensor_data():
        keys = ["N - Ratio of Nitrogen (NH4+) content in soil",
                "P - Ratio of Phosphorous (P) content in soil",
                "K - Ratio of Potassium (K) content in soil",
                "ph - Soil acidity (pH)",
                "ec - Electrical conductivity",
                "oc - Organic carbon",
                "S - Sulfur (S)",
                "zn - Zinc (Zn)",
                "fe - Iron (Fe)",
                "cu - Copper (Cu)",
                "Mn - Manganese (Mn)",
                "B - Boron (B)"]
        
        input_sensor = sensor_data[random.choice(list(sensor_data.keys()))]

        data_dict = {k:v for k,v in zip(keys,input_sensor)}

        return data_dict, input_sensor