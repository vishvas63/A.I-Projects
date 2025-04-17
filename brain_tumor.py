import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model("brain_tumor_model.h5")

st.title("Brain Tumor Detection App")
st.write("Upload an MRI scan image to check for brain tumors.")

# File upload
uploaded_file = st.file_uploader("Choose a brain MRI image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.resize(image, (150,150))
    image = image / 255.0
    image = image.reshape(1, 150, 150, 3)
    
    prediction = model.predict(image)
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    if prediction[0][0] > 0.5:
        st.write("### 🛑 Tumor Detected")
    else:
        st.write("### ✅ No Tumor Detected")
