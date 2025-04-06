![](https://github.com/gulabpatel/AIAg/blob/main/SmartAG/AugmentedStartupCourse/08_PestPrediction_app/PestPrediction.PNG)﻿
# Weather-Based Pest Prediction Application Documentation

## **Introduction**
The weather based pest prediction is an application helps farmers detect the type of pest affecting the particular plant and also make recommendations on the Choice of pesticide, Weather conditions for application, and Application method. 

It is a integration of a ReactJS frontend and a Python-powered backend. It also utilizes the YOLOv8 model, fine-tuned using the rice pest [dataset](https://universe.roboflow.com/laktharu/rice-pests-ztbeq).

## **Model Training**

### **Dataset Acquisition and Preparation**

1. Navigate to the provided [Roboflow dataset URL](https://universe.roboflow.com/laktharu/rice-pests-ztbeq).
2. Click on "Download Dataset" and select the YOLOv8 annotation format.
3. Opt for the "show download code" and copy the displayed code.
4. Integrate this code into a Colab notebook and execute it.
5. Dive into this directory and locate the `data.yaml` file. Adjust the paths for train, validation, and test images to their respective absolute directory paths.

### **Model Training Process**

1. Commence by installing the `ultralytics` package:
   ```bash
   pip install ultralytics
   ```
2. Adhere to the instructions available in the dedicated training tutorial to aptly train and evaluate the YOLOv8 model.
3. Upon concluding the training, ensure the `best.pt` weight file is saved within the `runs/detect/train/weights` directory.

## **Backend Configuration**

1. Initiate the setup by installing the necessary Python packages:
   ```bash
   pip install ultralytics langchain openai tiktoken flask Flask-cors geopy
   ```
2. Securely integrate your `OPENAI_API_KEY` into the script. Alternatively, you can set it as an environment variable:
   ```bash
   export OPENAI_API_KEY="INSERT_YOUR_API_KEY"
   ```
3. Securely integrate your `OPENWEATHER_API_KEY` into the script.

4. Refer to the dedicated backend tutorial to pen the backend script. It's paramount to ensure the `best.pt` weights are situated within the `assets` directory.

5. To activate the backend server, navigate to your application's root directory and execute:
   ```bash
   python app.py
   ```
   Ensure that the server starts successfully, typically indicating it's listening on a designated port (e.g., `localhost:5000`).


## **Frontend Development**

### **Setting Up the Environment**

1. Begin by installing the latest version of Node.js, tailored to your operating system.
2. install chart.js
   ```npm install chart.js
   ```
2. To initiate a fresh ReactJS application, execute
:
   ```bash
   npx create-react-app frontend
   ```
   However, if leveraging the code we've provided, simply install the requisite dependencies:
   ```bash
   npm install
   ```

### **Launching the Application**

Run your React application by executing:
```bash
npm start
```

This will launch the application in your default browser, typically accessible at `localhost:3000`.

**Note**: Always ensure your backend services are running and accessible for the frontend application to function optimally.
