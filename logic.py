import os
from keras.models import load_model
from keras.metrics import MeanAbsoluteError
import cv2
import numpy as np

def process_image(image_path):
    """
    Processes the input image and performs predictions using the model.
    """
    try:
        print(f"Processing image: {image_path}")  # Debugging

        model_path = "C:\\Users\\Asus\\Desktop\\Yantra2\\Backend\\model\\denoiser_cnn_epoch_30-gaussian.h5"
        if not os.path.exists(model_path):
            print("Model file not found!")
            return {"error": "Model file missing"}

        model = load_model(model_path, custom_objects={"mae": MeanAbsoluteError()})
        print("Model loaded successfully.")

        # Load and preprocess image
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print("Image load failed!")
            return {"error": "Failed to read image"}

        image = cv2.resize(image, (256, 256))
        image_array = image.astype('float32') / 255.0
        image_array = np.expand_dims(image_array, axis=(0, -1))

        # Perform prediction
        denoised_image_array = model.predict(image_array)[0]

        # Postprocess output
        denoised_image = (denoised_image_array.squeeze() * 255).astype(np.uint8)

        # Save the output image
        output_dir = os.path.join(os.path.dirname(__file__), "outputs")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "denoised_image.png")
        cv2.imwrite(output_path, denoised_image)

        if not os.path.exists(output_path):
            print("Error saving the output image!")
            return {"error": "Failed to save processed image"}

        print(f"Denoised image saved at: {output_path}")
        return output_path

    except Exception as e:
        print(f"Error in process_image: {e}")
        return {"error": str(e)}

