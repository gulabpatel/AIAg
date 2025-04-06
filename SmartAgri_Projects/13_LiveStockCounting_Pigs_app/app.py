import streamlit as st
import requests
from PIL import Image
import numpy as np
from inference.models.utils import get_roboflow_model
import cv2
import random
import time
import torch
from transformers import pipeline
from transformers.models.bert import BertTokenizer
from io import BytesIO

text2text_generator = pipeline("text2text-generation")
text2text_generator.model.config.model_max_length = 512

#############
##### Set up sidebar
#############

st.sidebar.write('#### Select an image to upload')
upload_file = st.sidebar.file_uploader('', type=['png','jpg','jpeg'], accept_multiple_files=False)

#############
### Set up main app
#############

## Title
st.write('# Pig Object Detection')
st.write('Please upload an image to the left to count the number of pigs in that image')

## Pull in default images or user-selected image.
if upload_file is None:
    # Default image
    st.write('Waiting...')
    url = 'https://images.unsplash.com/photo-1598635177046-eb7043682009?auto=format&fit=crop&q=60&w=500&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fHBpZ3N8ZW58MHx8MHx8fDA%3D'
    image = Image.open(requests.get(url, stream=True).raw)
    # image = pillow_simd.Image.open(requests.get(url, stream=True))
    # Read the response data into memory
    # image = BytesIO(image.content)
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
else:
    ## Pull user-selected image
    image = Image.open(upload_file)
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

## Subtitle
st.write('## Inference Image')

model = get_roboflow_model(
    model_id="pig-count/1",
    #Replace ROBOFLOW_API_KEY with your Roboflow API Key
    #api_key = "ROBOFLOW_API_KEY"  "rf_wTUVeovqxMEIWHCQhbnl", "ceRP3MCEYy4nieow2PL4"
    api_key = "ceRP3MCEYy4nieow2PL4"
)

results = model.infer(image=opencvImage, confidence=0.8, iou_threshold=0.85)

output = opencvImage.copy()
count = 0

# Plot image with face bounding box (using opencv)
for result in results[0]:
    bounding_box = results[0][count]
    print(bounding_box)

    x0, y0, x1, y1 = map(int, bounding_box[:4])

    cv2.rectangle(output, (x0, y0), (x1, y1), (255,255,0), 2)
    cv2.putText(output, "Pig",(x0,y0-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 2)
    count = count+1

color_converted = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

pil_image = Image.fromarray(color_converted)

## Display image
st.image(pil_image, use_column_width=True)

## Detection statements in main app
st.write('Number of pigs detected: ', count)

st.write("Welcome to the Question and Answer Chatbot. Let's talk about taking care of pigs.")
input = st.text_input("You detected "+str(count) +" pigs! Ask me something about them?")

if 'count' not in st.session_state or st.session_state.count == 6:
    st.session_state.count = 0
    st.session_state.chat_history_ids = None
    st.session_state.old_response = ''
else:
    st.session_state.count += 1

if input:
    # read whole file to a string
    context_input = "Pigs need regular healthcare, including veterinary check-ups, vacations, and protection against diseases like swine flu and foot-and-mouth disease. THey're social animals, so interaction with other pigs or humans is essential for their mental health. They also enjoy activities like playing with toys and listening to music, which enhance their well-being."

    response = text2text_generator('question: '+ input + 'context: ' + context_input)

    answer = response[0]['generated_text']
    print("Answer: ", answer)
    
    if answer =="":
        answer = "Sorry, I can't asnwer that."
    
    st.write("Chatbot: ", answer)
    st.session_state.old_response = answer
