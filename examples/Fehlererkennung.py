import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from matplotlib import pyplot as plt

model = load_model('defect_detection_model.h5')

def predict_defect(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (img_height, img_width))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)
    return "Defekt erkannt" if prediction[0][0] > 0.5 else "Kein Defekt erkannt"

def show_image_with_prediction(image_path):
    img = cv2.imread(image_path)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(predict_defect(image_path))
    plt.axis('off')
    plt.show()

test_image_path = 'test.bilder'
show_image_with_prediction(test_image_path)