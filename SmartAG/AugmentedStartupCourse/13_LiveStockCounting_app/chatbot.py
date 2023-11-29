import streamlit as st
import random
import time
import torch
from transformers import pipeline
from transformers.models.bert import BertTokenizer

text2text_generator = pipeline("text2text-generation")
# Set the maximum length of the generated text
text2text_generator.model.config.model_max_length = 512

st.write("### Welcome to the Question and answer chat bot. Let's talk about taking care of pigs")
input = st.text_input("Ask me something about the pigs")

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
