
# Import all the necessary libraries
import streamlit as st
import numpy as np
from PIL import Image  # For handling image files
import tensorflow as tf
import os
# import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader

# Apply custom CSS for layout and dark green sidebar
def add_custom_styles():
    st.markdown(
        """
        <style>

        /* Sidebar - Dark Green */
        section[data-testid="stSidebar"] {
            background-color: #1B5E20 !important; /* Dark Green */
        }
        
        /* Sidebar text color */
        section[data-testid="stSidebar"] * {
            color: white !important;
        }

        /* Input fields text color */
        .stTextInput>div>div>input, 
        .stNumberInput>div>div>input {
            color: black !important;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #555;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Call functions to apply styles
add_custom_styles()

work_dir = os.path.dirname(os.path.abspath(__file__))
model_path = f"{work_dir}/trained_cnn_model.keras"

# Tensorflow Model Prediction
# In this function first I wll load the model trained model, and I will be using the same parameters which was used in
# the Test.ipynb file.
# Next I will do the image preprocessing on the test images which was also used in the test file
# After doing the preprocessing step, I will do the model prediction

def model_prediction(test_image):
    cnn = tf.keras.models.load_model(model_path, compile=False, safe_mode=True) # Loading the model -used from test file
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))               # Preprocess the test image with target size (128, 128) which was used during model trainning
    input_arr = tf.keras.preprocessing.image.img_to_array(image)                                    # Convert the test images into array
    input_arr = np.array([input_arr])                                                               # Convert the array into batch

    prediction = cnn.predict(input_arr)          # Perform the prediction using cnn.predict() function into input_arr
    result_index=np.argmax(prediction)           # Get maximum value of the prediction
    return result_index


# Create Web App Sidebar
st.sidebar.title("🌿 Plant Disease Detection")
app_mode = st.sidebar.radio("Go to", ["Home", "About", "Detect Plant Disease", "Settings"])

# Home Page Content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.title("🌱 Welcome to Plant Disease Detection System")

if(app_mode=="Home"):
    st.header("Plant Disease Detection System!")
    image_path = "plant.jpeg"
    st.image(image_path,use_container_width=True)
    st.write("""
    Welcome to Plant Disease Detection System! 🌿

    This application is designed to detect plant diseases efficiently and effortlessly.
    Upload an image of a plant leaf, and the system will analyse it to detect potential diseases.

    """)

# Design About Page
elif(app_mode=="About"):
    st.header("About")
    st.subheader("ℹ️ About This App")
    st.write("""
    This application uses a Deep Learning model (Convolutional Neural Network)to analyse plant leaves and detect diseases.

    ## Steps to Analyse the Disease
    
    - **Navigate to "Detect Plant Disease" page**
    - **Browse the image for analysis**
    - **Use "Detect" button for analysis**
    - **Get the result immediately**
    
    """)


# Detection Page - the main page of this app
elif(app_mode=="Detect Plant Disease"):
    st.header("Detect Plant Disease")                        # Add the header of the page
    test_image = st.file_uploader("Upload an Image:")        # Use file_uploader() function for uploading the image in Streamlit
    if(st.button("Show Image")):                             # Create "Show Image" button
        st.image(test_image,width=4,use_container_width=True)   # If "Show Image" button pressed condition
    if(st.button("Detect")):                                 # Create the Detect button
        st.write("Prediction Result:")
        result_index = model_prediction(test_image)
        #Reading Labels
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
        st.success("Model is Predicting it's a {}".format(class_name[result_index]))


# Setting Page
elif app_mode == "Settings":
    st.subheader("⚙️ Settings")
    st.write("Modify your preferences here.")

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">© 2025 Plant Disease Detection</div>', unsafe_allow_html=True)
