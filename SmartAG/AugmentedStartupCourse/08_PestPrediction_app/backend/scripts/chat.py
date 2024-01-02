from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

import geopy
import requests
from geopy.geocoders import Nominatim

def getcoordinate(city):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    return (location.latitude, location.longitude)

def getweatherdata(day):
    Api_key = open('./openweather_api_key.txt', 'r').read()
    city = 'london'
    lat, lon = getcoordinate(city)

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={Api_key}&units=metric"

    res = requests.get(forecast_url).json()
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
    temp_max = current_data['main']['temp_max']
    temp_min = current_data['main']['temp_min']

    return (date, temperature, humidity, windspeed, pressure, description, temp_max, temp_min)

OPENAI_API_KEY = 'sk-yX4xO39wByOCGTqOuvmbT3BlbkFJPswlMS6hqZJFHLTGUf#####'      # use your key here

model_name = 'gpt-3.5-turbo'
# model_name = 'gpt-4'

llm = ChatOpenAI(model_name = model_name, temperature = 0.3, openai_api_key = OPENAI_API_KEY)

class_info_dict= {
    # Healthy Leaves
    "brown-planthopper": "The brown planthopper (Nilaparvata lugens) is a notorious agricultural pest that primarily affects rice crops.Brown planthoppers feed on the sap of rice plants by piercing and sucking through their needle-like mouthparts, leading to weakened plants and reduced yields. Commonly used classes of insecticides for controlling brown planthoppers include neonicotinoids, pyrethroids, and carbamates.For optimal pesticide application, aim for mild temperatures (60-85°F), low to moderate wind speeds (3-10 mph), and moderate humidity. Apply pesticides in the early morning or late afternoon, avoiding extreme weather conditions and ensuring adherence to specific label instructions for each pesticide",
    "green-leafhopper": "The green-leafhopper is a pest affecting crops like rice. Effective control often involves using neonicotinoid or pyrethroid insecticides. Optimal weather conditions for application include temperatures between 70-85°F, low wind speeds, and moderate humidity.",
    "leaf-folder": "The leaf-folder, a pest in rice cultivation, can be managed with systemic insecticides like neonicotinoids or with Bacillus thuringiensis (Bt) formulations. Apply during calm weather with temperatures around 75-85°F and low wind speeds for best results.",
    "rice-bug": "For controlling rice bugs, insecticides such as pyrethroids or neonicotinoids are effective. Optimal weather conditions for application include temperatures around 80°F, low to moderate wind speeds, and moderate humidity.",
    "stem-borer": "Stem-borers in crops like rice can be controlled with insecticides like carbamates or pyrethroids. Apply during temperatures of 75-85°F, low wind speeds, and moderate humidity for optimal efficacy.",
    "whorl-maggot": "To combat whorl-maggots in crops, use insecticides like neonicotinoids or organophosphates. Apply during temperatures of 70-80°F, low wind speeds, and moderate humidity for the best results.",
}

def chatbot(info, history, message, weather_data, gdd):

    date, temperature, humidity, windspeed, pressure, description, temp_max, temp_min = weather_data
    weather_info = {'date': date, 'temperature': temperature, 'humidity':humidity, 'pressure':pressure, 'description':description, 'maximum-temperature': temp_max, 'minimum-temperature': temp_min, 'windspeed':windspeed}
    
    prompt_template = """
    You are a farming expert with a specialized knowledge in pests affecting plants. you are provided with the current weather information in the city 
    as well as the value of the growing degree days(GDD) of the pest. A farmer comes to you with the name of a specific pest
    and some basic information about it. 
    
    Your job is to guide the farmer on how to control the pest stating the growing degree days,the choice of pesticide, optimum weather condition for application and also the application method. 
    inform the farmer if the current weather condition is not optimum for the application of the pesticide.  

    You response should be concise and orderly structured.  
    

    Information about the pest: {info},

    Weather information: {weather_info}

    Growing degree days: {gdd}

    Chat history: {history},

    User question: {message}

    """

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables= ['info', 'weather_info', 'gdd', 'history', 'message']
    )

    chain = LLMChain(llm=llm, prompt=PROMPT)

    response = chain.predict(info = info, weather_info= weather_info, gdd=gdd, history = history, message = message)

    return response