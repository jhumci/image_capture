import os
import numpy as np
import cv2
from matplotlib import pyplot as plt
from tensorflow.keras.models import load_model

# Parameter
img_height, img_width = 128, 128

# Funktion zur Vorhersage
def predict_defect(image_path, model):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (img_height, img_width))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)
    return "Defekt erkannt" if prediction[0][0] > 0.5 else "Kein Defekt erkannt"

# Funktion zur Anzeige des Bildes mit Vorhersage
def show_image_with_prediction(image_path, model):
    img = cv2.imread(image_path)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(predict_defect(image_path, model))
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # Modell laden
    model = load_model('defect_detection_model.h5')

    # Verzeichnis der hochgeladenen Bilder
    image_directory = "test.bilder/"
    image_files = [
        "images.jpeg",
        "images (1).jpeg",
        "images (2).jpeg",
        "images (3).jpeg",
        "Download (1).jpeg",
        "Download (2).jpeg"
    ]

    # Vorhersagen für jedes Bild anzeigen
    for image_file in image_files:
        image_path = os.path.join(image_directory, image_file)
        show_image_with_prediction(image_path, model)

