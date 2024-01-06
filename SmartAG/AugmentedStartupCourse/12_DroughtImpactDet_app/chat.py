# Import necessary modules and classes from langchain package
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# Define your OpenAI API key
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
    You are assisting a farmer with information on drought impact detection and its implications for agriculture.\
    Explain how farmers can use predictive knowledge to mitigate the effects of drought and protect their crops.\
    Offer practical advice, strategies, and resources that farmers can use to better prepare for and respond to drought conditions\
    
    Also, some input parameters about the soil will be provided to you\
    (do not ask the user for this information from user in chat). This information includes: \
    Surface Pressure (PS), Specific Humidity at 2 Meter (QV2M), Temperature at 2 Meters (T2M), Temperature Range at 2 Meters (T2MDEW), \
    Maximum Temperature at 2 Meters (T2M_MAX), Minimum Temperature at 2 Meters (T2M_MIN), Temperature Range at 2 Meters (T2M_RANGE), Earth Skin Temperature (TS), \
    Wind Speed at 10 Meters (WS10M), Wind Speed Range at 10 Meters (WS10M_RANGE), Wind Speed at 50 Meters (WS50M), Maximum Wind Speed at 50 Meters (WS50M_MAX), \
    Wind Speed Range at 50 Meters (WS50M_RANGE), YEAR, DATE. \
    There values are {info} respectively.\
    
    The prediction of the drought is {output} based on the input information about soil, here 0 corresponds to Abnormally Dry, 1 corresponds to Moderate Drought, \
    2 means Severe Drought, 3 means Extreme Drought and 4 means Exceptional Drought.
    
    Asked the user if they want generic information or specific crop related. Once you have chat history don not greet again,\
    perform your task based on the input parameters and drought prediction.\
    If the crop type is mentioned by the farmer, you have to provide crop-specific advice based on the drought prediction otherwise generic information.\
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
