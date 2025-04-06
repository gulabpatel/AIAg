import requests
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from string import Template

app = Flask(__name__)
CORS(app)

os.environ["OPENAI_API_KEY"]='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'  # Open AI key

crop_bot = None
conversation = None

def extract_essential_info(weather_data):
    essential_info = []

    for entry in weather_data["list"]:
        essential_entry = {
            "timestamp": entry["dt_txt"],
            "temperature": entry["main"]["temp"],
            "feels_like": entry["main"]["feels_like"],
            "weather_condition": entry["weather"][0]["main"],
            "weather_description": entry["weather"][0]["description"],
            "wind_speed": entry["wind"]["speed"],
            "wind_direction": entry["wind"]["deg"]
        }
        essential_info.append(essential_entry)

    return essential_info


# '/api/get-weather-analysis'
@app.route('/api/get-analysis', methods=['POST'])
def get_weather_analysis():

    if not request.json or 'forecast' not in request.json:
        return jsonify({'error': 'No forecast provided'}), 400
    if not request.json or 'crop' not in request.json:
        return jsonify({'error': 'No crop provided'}), 400
    if not request.json or 'stage' not in request.json:
        return jsonify({'error': 'No stage provided'}), 400
    
    global crop_bot
    global conversation
    crop_bot = ChatOpenAI()
    conversation = ConversationChain(llm=crop_bot)    
    api_data = request.get_json()
    crop, crop_stage = api_data['crop'],api_data['stage']
    data = api_data['forecast']
    city = data['city']['name']
    temperature = data['list'][0]['main']['temp']
    weather = data['list'][0]['weather'][0]['description']
    data = extract_essential_info(data)
    firstQuery = Template ("""
    You are an advanced chatbot dedicated to supporting farmers in optimizing crop yields. Your assistance is tailored to the specific agricultural context, considering the following parameters:
    - City Name: $city
    - Crop Type: $crop
    - Temperature (Celsius): $temperature
    - Current Weather: $weather
    - Crop Stage: $crop_stage
    - Weather forecast for the next 5 days: $forecast
    Your role is to generate insightful responses and recommendations to aid farmers in making informed decisions. Address the following aspects:
    1. Current Conditions:
    - Briefly describe the current weather conditions in $city, including temperature and any notable weather events.
    - Highlight the developmental stage of the specified crop ($crop_stage).
    2. Crop Recommendations:
    - Provide agriculture-related guidance based on the current conditions, considering the specific crop ($crop).
    - Include suggestions for irrigation, fertilization, and other cultivation practices that align with the crop stage.
    3. Worst Weather Conditions (Next 5 Days):
    - Inform the user about the anticipated worst weather conditions for the next 5 days.
    4. Protective Measures:
    - If there is a forecast of any adverse weather condition, offer protective measures for the specified crop. This may include sheltering suggestions, additional nutrients, or other relevant precautions.
    You don't need to introduce yourself or provide any additional information. Please make sure that you format your response in HTML format using <li>, <p>, etc wherever necessary.
    Your goal is to deliver a comprehensive and empathetic response, considering the unique challenges and opportunities presented by the combination of city, crop, and weather variables.
    Thank you for your assistance in supporting our farming community.
        """)
    response = conversation.run(firstQuery.substitute(city=city,weather=weather, crop=crop,crop_stage = crop_stage, temperature= temperature, forecast= data))
    return jsonify({'response': response}), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    if not request.json or 'message' not in request.json:
        return jsonify({'error': 'No message provided'}), 400
    data = request.get_json()
    user_message = data['message']
    bot_response = conversation.run(user_message)
    print(bot_response)
    return jsonify({'response': bot_response}), 200

if __name__ == '__main__':
    app.run(debug=True)

