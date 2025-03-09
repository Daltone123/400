import os
import numpy as np
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "saved_models", "dira_model.keras")
CLASS_NAMES = ["Early Blight", "Healthy", "Late Blight"]

# Load the model once to avoid reloading it multiple times
MODEL = tf.keras.models.load_model(MODEL_PATH)
