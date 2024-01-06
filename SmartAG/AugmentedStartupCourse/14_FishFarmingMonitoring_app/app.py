#Install dependencies
#pip install streamlit openai

#Set api key through command prompt/terminal
#export OPENAI_API_KEY=<YOUR_API_KEY>

#to run the app
#python -m streamlit run app.py or streamlit run app.py

import streamlit as st
# import openai
from openai import OpenAI
import os

# Initialize the OpenAI client
os.environ["OPENAI_API_KEY"] = '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'
openai = OpenAI()

# Streamlit app setup
st.set_page_config(page_title="Fish Farming Expert Chatbot", layout="wide")
st.title("Fish Farming Expert Chatbot")
st.write("Welcome to your personal fish farming expert chatbot app! Ask any question related to fish farming:")

# Function to interact with the latest GPT model
def generate_response(user_input, chat_history=None):
    if chat_history is None:
        chat_history = []

    system_message = {"role": "system", "content": "You are an assistant expert in fish farming."}
    messages = [system_message]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_input})

    response = openai.chat.completions.create(
        # model="ft:gpt-3.5-turbo-0613:personal::8Iay5z35",
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message.content 

# Callback function for generating response
def handle_response():
    user_input = st.session_state.user_input
    if user_input.strip() != "":
        response = generate_response(user_input, st.session_state.messages)
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""  # Clear the user input

# Chat history management
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Display chat history
st.write("Chat History")
with st.container():
    for message in st.session_state.messages:
        role = "You:" if message["role"] == "user" else "Expert:"
        st.text_area(role, value=message["content"], height=75, disabled=False, key=message["content"] + role)

# Move the input area to the bottom
with st.form(key='user_input_form'):
    user_input = st.text_area("Ask your question:", value=st.session_state.user_input, key="user_input")
    submit_button = st.form_submit_button(label='Get Answer', on_click=handle_response)
    if submit_button:
        handle_response()

st.markdown(
    """
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
        }
        /* Styling for chat history text areas */
        .stTextArea>div>div>textarea {
            background-color: #f8f9fa; /* Light grey background */
            color: #212529; /* Dark text for contrast */
            opacity: 1; /* No transparency */
            font-size: 16px; /* Adjust font size if necessary */
        }
        /* Styling for buttons */
        .stButton>button {
            background-color: #4CAF50; /* Green background for buttons */
            color: white; /* White text for buttons */
            font-weight: bold;
            margin: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

