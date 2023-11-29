from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

OPEN_API_KEY = ""
model_name = 'gpt-3.5-turbo'
#model_name = 'gpt-4'
OPEN_API_KEY='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'
llm = ChatOpenAI(model_name=model_name, temperature=0.3, openai_api_key=OPEN_API_KEY )


class_info_dict= {
    # Healthy Leaves
    "Apple leaf": "This represents a healthy apple leaf. Apple trees are deciduous and are widely grown for their delicious fruits.",
    "Bell_pepper leaf": "This represents a healthy bell pepper leaf. Bell peppers are a variety of Capsicum annuum and are grown for their fruits which are used in cooking.",
    "Blueberry leaf": "This represents a healthy blueberry leaf. Blueberries are small shrubs that produce berries rich in antioxidants.",
    "Cherry leaf": "This represents a healthy cherry leaf. Cherry trees produce small, round fruits that are usually red or black.",
    "Corn leaf": "This represents a healthy corn leaf. Corn is an important cereal crop that is used for both human consumption and livestock feed.",
    "Peach leaf": "This represents a healthy peach leaf. Peach trees produce sweet, juicy fruits and are grown in temperate climates.",
    "Potato leaf": "This represents a healthy potato leaf. Potatoes are tuberous crops that are a staple food in many countries.",
    "Raspberry leaf": "This represents a healthy raspberry leaf. Raspberry plants produce small, red or black berries that are rich in nutrients.",
    "Soybean leaf": "This is a healthy soybean leaf. Soybeans are leguminous plants and a significant source of protein and oil.",
    "Strawberry leaf": "This represents a healthy strawberry leaf. Strawberry plants are known for their sweet, red fruits.",
    "Tomato leaf": "This represents a healthy tomato leaf. Tomato plants produce red or yellow fruits that are a key ingredient in many dishes.",
    "Grape leaf": "Represents a healthy grape leaf. Grapes are grown for both eating and wine production.",

    # Diseased Leaves
    "Apple Scab Leaf": "Apple scab is a disease caused by the fungus Venturia inaequalis. It creates dark, scab-like lesions on leaves.",
    "Apple rust leaf": "Apple rust is caused by various types of fungi and results in yellow-orange spots on leaves.",
    "Bell_pepper leaf spot": "This is a fungal or bacterial disease that causes small, dark spots on bell pepper leaves.",
    "Corn Gray leaf spot": "Caused by the fungus Cercospora zeae-maydis, it results in rectangular gray spots on corn leaves.",
    "Corn leaf blight": "This is caused by the fungus Helminthosporium maydis and leads to long grayish streaks on corn leaves.",
    "Corn rust leaf": "This disease is caused by the fungus Puccinia sorghi and leads to rust-like spots on corn leaves.",
    "Potato leaf early blight": "Caused by the fungus Alternaria solani, it results in dark spots on potato leaves.",
    "Potato leaf late blight": "This is caused by the oomycete Phytophthora infestans and can lead to large, dark lesions on potato leaves.",
    "Squash Powdery mildew leaf": "This disease is characterized by white powdery spots and is caused by various species of fungi.",
    "Tomato Early blight leaf": "This is caused by the fungus Alternaria solani and leads to dark spots on tomato leaves.",
    "Tomato Septoria leaf spot": "Caused by the fungus Septoria lycopersici, it results in small, dark spots with light centers on tomato leaves.",
    "Tomato leaf bacterial spot": "This is caused by bacteria and results in small, necrotic spots on tomato leaves.",
    "Tomato leaf late blight": "Similar to potato late blight, this is caused by Phytophthora infestans.",
    "Tomato leaf mosaic virus": "This viral disease leads to distorted and mottled leaves.",
    "Tomato leaf yellow virus": "A viral disease that results in yellowing and curling of tomato leaves.",
    "Tomato mold leaf": "This could be caused by various types of mold fungi and results in a fuzzy growth on tomato leaves.",
    "Tomato two spotted spider mites leaf": "This is an infestation rather than a disease, caused by the two-spotted spider mite. It results in stippling and discoloration of leaves.",
    "Grape leaf black rot": "Caused by the fungus Guignardia bidwellii, it leads to black spots on grape leaves."
}

def chatbot(info, history, message):
    prompt_template = """
    You are a farming expert with a specialized knowledge in plant diseases. A farmer comes to you with the name of specific plant disease
    and some basic information about it. Your job is to guide the farmer.

    Information about the disease: {info},

    Chat history: {history}

    User question: {message}
    """

    PROMPT = PromptTemplate(
        template = prompt_template,
        input_variables = ['info', 'history', 'message']
    )

    chain = LLMChain(llm=llm, prompt=PROMPT)

    response = chain.predict(info = info, history = history, message = message)
    return response


