from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import os
import requests


app = FastAPI()

# Trained model path
work_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(work_dir, "trained_cnn_model.keras")

endpoints =

# Load trained model
cnn = tf.keras.models.load_model(model_path, compile=False, safe_mode=True)
print(f"✅ Model Loaded Successfully! Expected Input Shape: {cnn.input_shape}")

# Class labels
class_name = ['Apple___Apple_scab',
 'Apple___Black_rot',
 'Apple___Cedar_apple_rust',
 'Apple___healthy',
 'Blueberry___healthy',
 'Cherry_(including_sour)___Powdery_mildew',
 'Cherry_(including_sour)___healthy',
 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
 'Corn_(maize)___Common_rust_',
 'Corn_(maize)___Northern_Leaf_Blight',
 'Corn_(maize)___healthy',
 'Grape___Black_rot',
 'Grape___Esca_(Black_Measles)',
 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
 'Grape___healthy',
 'Orange___Haunglongbing_(Citrus_greening)',
 'Peach___Bacterial_spot',
 'Peach___healthy',
 'Pepper,_bell___Bacterial_spot',
 'Pepper,_bell___healthy',
 'Potato___Early_blight',
 'Potato___Late_blight',
 'Potato___healthy',
 'Raspberry___healthy',
 'Soybean___healthy',
 'Squash___Powdery_mildew',
 'Strawberry___Leaf_scorch',
 'Strawberry___healthy',
 'Tomato___Bacterial_spot',
 'Tomato___Early_blight',
 'Tomato___Late_blight',
 'Tomato___Leaf_Mold',
 'Tomato___Septoria_leaf_spot',
 'Tomato___Spider_mites Two-spotted_spider_mite',
 'Tomato___Target_Spot',
 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
 'Tomato___Tomato_mosaic_virus',
 'Tomato___healthy']

# Ping API to check if the server is running
@app.get("/ping")
async def ping():
    return {"message": "Hello, Server is running!"}

# Function to preprocess the image before model prediction
def preprocess_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data)).convert("RGB")  # Convert to RGB (if not already)
    image = image.resize((128, 128))  # Resize to match model's expected input size
    image = np.array(image, dtype=np.float32)  # Convert to NumPy array
    image = np.expand_dims(image, axis=0)  # Add batch dimension -> (1, 128, 128, 3)
    return image

# Prediction API
@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    # Read and preprocess the image
    image_data = await file.read()
    processed_image = preprocess_image(image_data)

    json_data = {

    }

    # Make prediction
    #predictions = cnn.predict(processed_image)
    requests.post(endpoints, json=json_data)
    result_index = np.argmax(predictions)  # Get class index
    confidence = float(np.max(predictions))  # Get confidence score

    return {
        "class": class_name[result_index],
        "confidence": confidence
    }

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=3000)
