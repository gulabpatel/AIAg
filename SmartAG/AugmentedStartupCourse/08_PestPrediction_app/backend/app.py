from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import io
from scripts.inference import inference as inferenceYOLO
from scripts.chat import chatbot, class_info_dict, getweatherdata

app = Flask(__name__)

CORS(app)

labels = []
classes = dict()
global weather_data
weather_data = getweatherdata('Today')

def calculate_gdd():
    temp_min, temp_max = weather_data[-2:]
    t_base = 10
    GDD = ((temp_min+temp_max)/2) - t_base
    return GDD


def detect(image):
    inferencedImage, classesInDataset, classesInImage = inferenceYOLO(image)
    imageClassesList = list(set(classesInImage))
    label = ""

    for x in range(len(imageClassesList)):
        if x>=len(imageClassesList) - 1:
            label = label + str(classesInDataset[imageClassesList[x]])
        else:    
            label = label + str(classesInDataset[imageClassesList[x]]) + ", "

    global labels 
    labels = imageClassesList
    global classes 
    classes = classesInDataset
    
    return inferencedImage, label

def chatfront(history, message):
    gdd = calculate_gdd()

    info = ""

    for x in range(len(labels)):
        name = str(classes[labels[x]])
        infoCurrent = str(class_info_dict[name])

        if x >= len(labels) - 1:
            info = info + name + ":" + infoCurrent
        else:
            info = info + name + ":" + infoCurrent + ", "

    response = chatbot(info, history, message, weather_data, gdd)

    return response

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': "No selected file"}), 400
    
    if file:
        in_memory_file = io.BytesIO()
        file.save(in_memory_file)
        data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv2.imdecode(data, color_image_flag)

        detected_image, label = detect(img)

        _, img_encoded = cv2.imencode('.jpg', detected_image)
        image_as_text = base64.b64encode(img_encoded).decode('utf-8')
        
        return jsonify({'image': image_as_text, 'label': label})
    
    return jsonify({'error': 'Failed to process the image'}), 500

@app.route('/chat', methods=["POST"])
def chat():
    if not request.json or 'message' not in request.json:
        return jsonify({'error': 'No message provided'}), 400
    
    data = request.get_json()

    user_message = data['message']
    chat_history = data['chatHistory']
    
    botResponse = f"{chatfront(chat_history, user_message)}"

    return jsonify({'response': botResponse})

if __name__ == '__main__':
    app.run(debug=True)