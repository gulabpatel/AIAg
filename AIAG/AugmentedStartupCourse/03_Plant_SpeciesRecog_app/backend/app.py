from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import json
import numpy as np
import io
from string import Template
from ultralytics import YOLO
from embedchain import App
from scripts.url import get_relevant_url

# os.environ["OPENAI_API_KEY"]='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'
os.environ["OPENAI_API_KEY"]='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'
app = Flask(__name__)
CORS(app)


model = YOLO("assets/best.pt")
botanist_bot = None

with open("assets/plantnet300K_species_id_2_name.json", 'r') as file:
    class_dict = json.load(file)

def inference(image):
    results = model(image)
    map_dict = results[0].names
    label = class_dict[map_dict[results[0].probs.top1]]
    return label


@app.route('/chat', methods=['POST'])
def chat():
    if not request.json or 'message' not in request.json:
        return jsonify({'error': 'No message provided'}), 400
    
    data = request.get_json()
    user_message = data['message']

    bot_response = botanist_bot.chat(user_message)

    return jsonify({'response': bot_response})


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        in_memory_file = io.BytesIO()
        file.save(in_memory_file)
        data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv2.imdecode(data, color_image_flag)

        label = inference(img)
        url = get_relevant_url(label)
        
        global botanist_bot

        botanist_bot = App()
        botanist_bot.add(url)

        first_query = Template("""
                Botanist Bot: Plant Information Service
                            
                Plant name: $name
                            
                Please provide the following details about the plant:
                - Brief Introduction to the plant
                - Scientific name
                - Native habitat
                - Ideal growing conditions (soil type, sunlight, water requirements, etc.)
                - Interesting facts (historical uses, unique characteristics, etc.)
                - Any other useful information
                
                Thank you!

                """
        )

        info = botanist_bot.chat(first_query.substitute(name=label))

        return jsonify({'label': label, 'info': info})
    
    return jsonify({'error': 'Failed to process the image'}), 500


if __name__ == '__main__':
    app.run(debug=True)


    

