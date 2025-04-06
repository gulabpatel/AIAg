# Import necessary modules and classes from FastAPI and other libraries
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import joblib
import numpy as np
from pathlib import Path
import json
from sklearn.preprocessing import StandardScaler

# Import the chatbot function from a separate module named 'chat'
from chat import chatbot

# Import the uvicorn server for running the FastAPI app
import uvicorn

# Create an instance of the FastAPI class
app = FastAPI()

# Load the RF model from the pickle file
model = joblib.load("model.pkl")

# Create a Pydantic model to define the request payload for drought prediction
class IrrigationDataRequest(BaseModel):
    SM: float
    TEMP: float
    SH: float
    AT: float
    WS: float
    AH: float
    WG: float
    P: float

# Configure static files (e.g., CSS, JavaScript)
app.mount("/static", StaticFiles(directory=Path("static")), name="static")

# Configure templates for HTML rendering (if using a template engine like Jinja2)
templates = Jinja2Templates(directory="templates")

output = None
# Define a function to make predictions for drought
def predict_drought(features: IrrigationDataRequest):
    global output  # Use the global variable
    # Convert input features to a NumPy array
    input_data = np.array(list(features.dict().values())).reshape(1, -1)
    
    # Create a new StandardScaler instance
    scaler = StandardScaler()
    
    # Fit the scaler to the input data (assuming you have enough data to fit it)
    scaler.fit(input_data)
    
    # Apply scaling to the input data
    scaled_input_data = scaler.transform(input_data)
    
    # Make predictions using the loaded RF model
    prediction = model.predict(scaled_input_data)
   
    output= int(prediction[0])
    print(output)
    # Return the predicted potability as 0 or 1 
    return output

# Create an endpoint to serve the HTML input form
@app.get("/")
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "prediction": None})

# Create an endpoint to receive POST requests with input data for drought prediction
@app.post("/predict")
async def predict(request: Request, json_data: str = Form(...)):
    features = json.loads(json_data)
    # Call the predict_drought function to make predictions
    prediction = predict_drought(IrrigationDataRequest(**features))
    
    # Render the HTML template with the prediction result
    return templates.TemplateResponse("index.html", {"request": request, "prediction": prediction})

# Create a Pydantic model to define the request payload for chatbot interactions
class ChatRequest(BaseModel):
    info: dict
    history: str
    message: str

# Create an endpoint to receive POST requests for chatbot interactions
@app.post("/chatbot/")
async def get_chatbot_response(chat_request: ChatRequest):
    print("history:", chat_request.history)
    try:
        # Call the chatbot function to generate a response
        response = chatbot(
            chat_request.info,
            chat_request.history,
            chat_request.message,
            output
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return response

# Run the FastAPI app using the uvicorn server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
