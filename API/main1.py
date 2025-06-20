from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

# Load trained model
CNN = tf.keras.models.load_model("trained_cnn_model.keras")

# Class names
class_name = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight',
    'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight',
    'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]

@app.get("/ping")
async def ping():
    return {"message": "Hello"}

# Read image file and convert to numpy array
def read_image_file(data) -> np.ndarray:
    image = Image.open(BytesIO(data)).convert("RGB")  # Ensure RGB
    return np.array(image)

# Preprocess image
def preprocess_image(image, target_size=(128, 128)):
    img = Image.fromarray(image).resize(target_size)
    img_array = np.array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    try:
        print("Received file:", file.filename)

        # Read image
        image_data = await file.read()
        print("File read successfully")

        # Convert to numpy array
        image = read_image_file(image_data)
        print("Image converted to numpy array:", image.shape)

        # Preprocess image
        image_batch = preprocess_image(image)
        print(f"Image batch shape: {image_batch.shape}")

        # Predict
        predictions = CNN.predict(image_batch)
        print("Prediction made:", predictions)

        # Get predicted class & confidence
        predicted_class = class_name[np.argmax(predictions[0])]
        confidence = np.max(predictions[0])
        print(f" Predicted: {predicted_class} with confidence {confidence:.2f}")

        return {
            'class': predicted_class,
            'confidence': float(confidence)
        }

    except Exception as e:
        print(f" Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
