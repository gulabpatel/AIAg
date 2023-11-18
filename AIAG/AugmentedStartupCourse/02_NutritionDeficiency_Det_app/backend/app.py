from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import numpy as np
import io
from string import Template
from ultralytics import YOLO
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain  

# os.environ["OPENAI_API_KEY"]='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'
os.environ["OPENAI_API_KEY"]='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'

app = Flask(__name__)
CORS(app)


model = YOLO("assets/best.pt")
botanist_bot = None

def inference(image):
    results = model(image)
    map_dict = results[0].names
    label = map_dict[results[0].probs.top1]
    return label


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
        botanist_bot = ChatOpenAI()
        first_query = Template("""
                Nutrient Deficiency Bot: Rice Nutrient Deficiency Information
                            
                Deficiency: $name
                            
                - Describe the visual symptoms associated with this deficiency.
                - Explain how this deficiency affects the overall health and growth of rice crops.
                - Provide recommendations or strategies for addressing and correcting this specific deficiency, which can help improve crop health and productivity.
                
                Thank you!

                """
        )
        global conversation
        conversation = ConversationChain(llm=botanist_bot)  
        info = conversation.run(first_query.substitute(name=label))

        return jsonify({'label': label, 'info': info})
    
    return jsonify({'error': 'Failed to process the image'}), 500


@app.route('/chat', methods=['POST'])
def chat():
    if not request.json or 'message' not in request.json:
        return jsonify({'error': 'No message provided'}), 400
    
    data = request.get_json()
    user_message = data['message']

    bot_response = conversation.run(user_message)
    return jsonify({'response': bot_response})


if __name__ == '__main__':
    app.run(debug=True)
