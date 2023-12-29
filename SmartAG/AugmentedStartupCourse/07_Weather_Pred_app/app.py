import os
import json
import docx
import geopy
import requests
from PIL import Image
import streamlit as st
from geopy.geocoders import Nominatim
from streamlit_chat import message
from string import Template
from embedchain import App
from embedchain.config import LlmConfig
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = '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'

def getcoordinate(city):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    return (location.latitude, location.longitude)

@st.cache_resource
def getweatherdata(day):
    Api_key = open('openweather_api_key.txt', 'r').read()
    city = 'Portharcourt, Nigeria'
    lat, lon = getcoordinate(city)
    # url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={Api_key}&units=metric"
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={Api_key}&units=metric"
    res = requests.get(forecast_url).json()
    print("res: ", res)
    day_map = {'Today':0, 'Tommorrow':8, '2 days': 16, '3 days': 24, '4 days': 32}
    idx = day_map[day]
    # extract weather information
    current_data = res['list'][idx]
    date = current_data['dt_txt'].split(" ")[0]
    temperature = current_data['main']['temp']
    pressure = current_data['main']['pressure']
    humidity = current_data['main']['humidity']
    description = current_data['weather'][0]['description']
    windspeed = current_data['wind']['speed']
    return (date, temperature, humidity, windspeed, pressure, description)

def extract_docx_content(docx_file):
    # Load the DOCX file
    doc = docx.Document(docx_file)
    # Initialize an empty string to store the content
    content = ""
    
    # Iterate through paragraphs in the document and extract text
    for paragraph in doc.paragraphs:
        content += paragraph.text + "\n" 
    return content

@st.cache_resource
def createbot (content):
    weather_chat_bot = App()
    weather_chat_bot.add(content)
    return weather_chat_bot
    
def get_response(content, current_data, query, start_conversation=False, history=None, schedules=None, user_message=None):

    #initialize the embedchain bot
    weather_chat_bot = createbot(content=content)
    # weather_chat_bot.add(content)

    if start_conversation:
            conversatiion_template  = Template( 
            f"""
                The following is a friendly conversation between human and an activity schedule assistant that help farmer schedules their activities. 
                The user can ask about his past activity schedules. he can also ask some clarification about the details of the activities. 
                use your own knowledge to answer those questions. 

                Relevant pieces of previous conversations:
                {history},

                All the previous activity schedules:
                Context: $context
                {schedules},

                current conversation:
                Human: $query
                Human: {user_message}
                schedule asistant ;

            """
    )
            llm_config = LlmConfig(stream=False, template=conversatiion_template, system_prompt="you are aa conversational chatbot.")
            response = weather_chat_bot.query(user_message, config=llm_config)

    else:
        #get weather information for other days
        tm_date, tm_temperature, tm_humidity, tm_windspeed, tm_pressure, tm_description = getweatherdata('Tommorrow')
        d2_date, d2_temperature, d2_humidity, d2_windspeed, d2_pressure, d2_description = getweatherdata('2 days')
        d3_date, d3_temperature, d3_humidity, d3_windspeed, d3_pressure, d3_description = getweatherdata('3 days')
        d4_date, d4_temperature, d4_humidity, d4_windspeed, d4_pressure, d4_description = getweatherdata('4 days')

        weather_chat_template = Template(
                f"""you are an activity scheduler and manager. you help farmers plan their activities based on the local weather pattern and information. 
                The user has uploaded a document containing a list of farming activities for a specific date and time. Additionally, the system has   
                retrieved the following (up to 4 days) local weather information for the same location from a weather API: date, Temperature, Humidity, Wind Speed,
                and Atmospheric Pressure. 
                                            
                    Document Content (Farming Activities): 
                    Context: $context
                    {content}
                    
                    Current Local Weather Information:
                    - date: {current_data[0]}
                    - current weather description: {current_data[5]}
                    - Temperature: {current_data[1]} °C
                    - Humidity: {current_data[2]} %
                    - Wind Speed: {current_data[3]} mph
                    - Atmospheric Pressure: {current_data[4]} hPa

                    Weather Information for Tommorrow:
                    - date: {tm_date}
                    - current weather description: {tm_description}
                    - Temperature: {tm_temperature} °C
                    - Humidity: {tm_humidity} %
                    - Wind Speed: {tm_windspeed} mph
                    - Atmospheric Pressure: {tm_pressure} hPa

                    Weather Information for 2 days time:
                    - date: {d2_date}
                    - current weather description: {d2_description}
                    - Temperature: {d2_temperature} °C
                    - Humidity: {d2_humidity} %
                    - Wind Speed: {d2_windspeed} mph
                    - Atmospheric Pressure: {d2_pressure} hPa

                    Weather Information for 3 days time:
                    - date: {d3_date}
                    - current weather description: {d3_description}
                    - Temperature: {d3_temperature} °C
                    - Humidity: {d3_humidity} %
                    - Wind Speed: {d3_windspeed} mph
                    - Atmospheric Pressure: {d3_pressure} hPa

                    Weather Information for 4 days time:
                    - date: {d4_date}
                    - current weather description: {d4_description}
                    - Temperature: {d4_temperature} °C
                    - Humidity: {d4_humidity} %
                    - Wind Speed: {d4_windspeed} mph
                    - Atmospheric Pressure: {d4_pressure} hPa
            
                    Based on the provided farming activities and local weather information, please generate an updated schedule that optimizes the following criteria:
                    1. Ensure the safety of farmers by considering weather conditions. For example, avoid outdoor activities during extreme weather events.
                    2. Optimize productivity by rescheduling activities that are weather-dependent to times or days when weather conditions are favorable.
                    3. Minimize potential damage to crops or equipment by avoiding activities that could be negatively impacted by the current weather conditions.
                    4. Prioritize urgent or time-sensitive activities.
                    5. Activities that requires the use of sun, activities such as sun drying must be re-scheduled to times when the sun still shines not evening.  
                    
                    Please provide a revised schedule in the form that includes the adjusted start times for farming activities,
                    if any, and any additional recommendations or notes based on the weather conditions. Ensure that the updated schedule aligns with the criteria mentioned above.
                    
                    Human: $query

                    Example Output (LLM Response):prompt := st.chat_input(placeholder='Ask me a question. e.g what activity is scheduled for 2pm') 
                    - Activity 1 (Original Start Time: [Original Start Time]): Recommended Start Time: [Updated Start Time]
                    - Activity 2 (Original Start Time: [Original Start Time]): Recommended Start Time: [Updated Start Time]
                    - Activity 3 (Original Start Time: [Original Start Time]): Recommended Start Time: [Updated Start Time]


                    [Additional recommendations or notes based on weather conditions.]
                """
            )

            # Example: Use the template, also add a system prompt.
        llm_config = LlmConfig(stream=False, template=weather_chat_template, system_prompt="you are an activity scheduler and manager.")
        response = weather_chat_bot.query(query, config=llm_config)
     
    return response

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []


def main ():
    
    st.set_page_config(page_title="WEATHER PREDICTION MODEL")
    st.header("Weather Prediction Model:memo:")
    st.caption('_your activity schedule assistant_')
    st.markdown(
        """
    <style>
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 350px;
        margin-left: -350px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    image = Image.open('logo2.PNG')
    st.sidebar.image(image)

    st.sidebar.markdown('---')
    activity_plan = st.sidebar.file_uploader("upload your activity plan", accept_multiple_files = True)
    st.sidebar.markdown('---')
    day = st.sidebar.selectbox(label='when would you like to schedule for?', 
                               options=['Today','Tommorrow', '2 days', '3 days', '4 days'], placeholder='Today'
                               )
    st.sidebar.markdown('---')

   

    if day:
        date, temperature, humidity, windspeed, pressure, description = getweatherdata(day)
        current_data = (date, temperature, humidity, windspeed, pressure, description)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Temperature", f"{temperature} °C", f'{description}')
    col2.metric("Humidity", f"{humidity} %", '4%')
    col3.metric("Windspeed", f"{windspeed} mph", '-8%')
    col4.metric("pressure", f"{pressure}")

    st.header('Scheduled Activity Board', divider = 'rainbow')

    if activity_plan:
        data_type = activity_plan[0].name.split('.')[-1]

        for doc in activity_plan:
            if data_type == 'docx':
                content = extract_docx_content(doc)

        query = "Please provide a revised schedule that includes the adjusted start times for farming activities"
        chatbot_response = get_response(content= content, current_data= current_data, query=query)

        st.text_area("_Revised Schedule_",chatbot_response)

        for i, chat_message in enumerate(st.session_state.conversation_history):
            is_user_message = chat_message['sender'] == 'User'
            message(chat_message['message'], is_user=is_user_message, key = str(i)+ ("_user" if is_user_message else ""))


        if user_message :=st.chat_input(placeholder='Ask me a question. e.g what activity is scheduled for 2pm'):
            chatbot_response = get_response(content= content, 
                                            current_data= current_data, 
                                            query=query,
                                            start_conversation=True, 
                                            history=st.session_state.conversation_history, 
                                            schedules=chatbot_response, 
                                            user_message=user_message)
            st.session_state.conversation_history.append({'sender': 'User', 'message': user_message})
            st.session_state.conversation_history.append({'sender': 'chatbot', 'message': chatbot_response})
            st.rerun()


if __name__ == "__main__":
    main()