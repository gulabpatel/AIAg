# Import necessary modules and classes from langchain package
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# Define your OpenAI API key
# OPENAI_API_KEY = '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'
OPENAI_API_KEY ='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'

# Define the model name you want to use. You can choose between 'gpt-3.5-turbo' and 'gpt-4'.
model_name = 'gpt-3.5-turbo'
# model_name = 'gpt-4'

# Create a ChatOpenAI instance with the chosen model and API key
llm = ChatOpenAI(model_name=model_name, temperature=0.3, openai_api_key=OPENAI_API_KEY)

# Define a chatbot function that takes input information, chat history, and user message
def chatbot(info, history, message, output):
    # Define a template for prompts with placeholders for user information, history, and message
    prompt_template = """
    You are assisting a farmer with information on water irrigation optimization and its implications for agriculture.\
    Explain how farmers can use predictive knowledge to increase their crops.\
    Offer practical advice, strategies, and resources that farmers can use.\
    
    Also, some input parameters about the soil and weather will be provided to you\
    (do not ask the user for this information from user in chat). This information includes: \
    soil_moisture, temperature, soil_humidity, air_temperature, wind_speed, air_humidity, wind_gust, pressure \
    There values are {info} respectively.\
    
    The prediction of the water suppy is {output} based on the input information about soil and weather,\
    here 0 corresponds to off and 1 corresponds to on.
    
    Asked the user if they want generic information or specific crop related. Once you have chat history do not greet again,\
    perform your task based on the input parameters and water supply prediction.\
    If the crop type is mentioned by the farmer, you have to provide crop-specific advice based on the water supply prediction otherwise generic information.\
    Your responses should be precise and have a human conversational touch.\
    Do not generate responses until the farmer provides you with the information.\
    
    Chat history: {history},
    User question: {message}
    
    If the user asks anything outside of this scope, display the message:I cannot provide you answers outside of the scope except replying to bye and thanks.
    """

    # Create a PromptTemplate with the defined template and input variables
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=['info', 'history', 'message', 'output']
    )

    # Create an LLMChain instance with the ChatOpenAI model and the defined prompt
    chain = LLMChain(llm=llm, prompt=PROMPT)

    # Generate a response using the chain and return it
    response = chain.predict(info=info, history=history, message=message, output=output)

    return response
