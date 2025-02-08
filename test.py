import tensorflow as tf
import numpy as np
import cv2
import os
from tensorflow.keras.losses import MeanAbsoluteError
from tensorflow.keras.models import load_model

# Load the trained Keras model
model_path = r"C:\\Users\santh\\.vscode\\Programming\\Yantra\\denoiser_cnn_epoch_30-gaussian.h5"
model = load_model(model_path, custom_objects={"mae": MeanAbsoluteError()})

print("Model loaded successfully!")

# Image preprocessing function
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was successfully loaded
    if img is None:
        raise FileNotFoundError(f"Error: Could not read image at {image_path}. Check the file path!")

    img = cv2.resize(img, (256, 256))  # Resize to match model input size
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=(0, -1))  # Add batch & channel dimensions
    return img

# Function to predict and save the denoised image
def predict_and_save(image_path, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    
    input_image = preprocess_image(image_path)
    output_image = model.predict(input_image)[0]  # Get model prediction

    # Convert output back to 8-bit image
    output_image = (output_image.squeeze() * 255).astype(np.uint8)
    output_path = os.path.join(output_dir, os.path.basename(image_path))
    
    cv2.imwrite(output_path, output_image)
    print(f"Denoised image saved at: {output_path}")
    return output_path

# Example usage
if __name__ == "__main__":
    image_path = r"Yantra/Gauss_1.2.826.0.1.3680043.8.498.11722494914277047769354284812925688733-c.png"
    predict_and_save(image_path)
