from flask import Flask, jsonify, request
import random
from flask_cors import CORS
import json
from scripts.infer import info_response, get_sensor_data, chat_response_user

app = Flask(__name__)
CORS(app)

@app.route('/get_sensor_data', methods=['GET'])
def get_sensor_data_route():
    data_dict, input_sensor = get_sensor_data()
    return jsonify(data_dict)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    history = data['history']
    message = data['message']
    first_message = data['first_message']
    
    print(data)
    
    if first_message:
        response = info_response(list(json.loads(data['message']).values()))
    
    else:
        response = chat_response_user(history, message)
    
    return jsonify(response)
    
    
if __name__ == "__main__":
    app.run(debug=True)