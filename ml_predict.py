import tensorflow as tf
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image



model = tf.keras.models.load_model(r"C:\Users\Pooja\OneDrive\Desktop\SIHfinal2025\SIH\water_waste_model_fixed.h5", compile=False)



def preprocess_image(img_path, target_size=(224, 224)):
    # 1. Load and resize image
    img = image.load_img(img_path, target_size=target_size)
    # 2. Convert to array
    img_array = image.img_to_array(img)
    # 3. Expand dimensions to make batch of 1
    img_array = np.expand_dims(img_array, axis=0)
    # 4. Normalize pixel values (if model trained on 0-1 range)
    img_array /= 255.0
    return img_array

def is_water_waste(img_path):
    # Preprocess
    img_array = preprocess_image(img_path, target_size=(224, 224))
    
    # Predict
    pred = model.predict(img_array)  # Returns a probability [[0.8]]
    
    # Convert to label
    if pred[0][0] > 0.5:
        return True   # Water-waste image
    else:
        return False  # Not water-waste
