import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from matplotlib import pyplot as plt

# Lege die Bildhöhe und -breite fest, auf die das Bild beim Lesen skaliert werden soll
img_height = 128
img_width = 128

# Lade das bereits trainierte Keras-Modell
model_path = 'defect_detection_model.h5'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Das Modell '{model_path}' wurde nicht gefunden.")

model = load_model(model_path)

def predict_defect(image_path):
    """
    Liest ein Bild ein, verarbeitet es auf die richtige Größe und führt eine Vorhersage durch.
    Gibt den String "Defekt erkannt" oder "Kein Defekt erkannt" zurück.
    """
    if not os.path.exists(image_path):
        return "Bild nicht gefunden"

    # Bild mit OpenCV lesen (BGR-Format)
    img = cv2.imread(image_path)

    # Auf die gewünschten Abmessungen skalieren
    img = cv2.resize(img, (img_height, img_width))

    # Auf [0,1]-Wertebereich normalisieren
    img = img / 255.0

    # Da das Modell eine Batch-Dimension erwartet, erweitern wir die Dimensionen
    img = np.expand_dims(img, axis=0)

    # Vorhersage durch das Modell
    prediction = model.predict(img)

    # Hier wird angenommen, dass prediction.shape = (1,1) (binäre Klassifikation).
    # Falls du mehrere Klassen hast, musst du die Auswertung anpassen.
    if prediction[0][0] > 0.5:
        return "Defekt erkannt"
    else:
        return "Kein Defekt erkannt"


def show_image_with_prediction(image_path):
    """
    Zeigt das Bild mit Matplotlib und schreibt das Ergebnis der Vorhersage in den Titel.
    """
    # Falls das Bild nicht existiert, Fehlermeldung ausgeben
    if not os.path.exists(image_path):
        print(f"Das Bild '{image_path}' wurde nicht gefunden.")
        return

    # Bild im BGR-Format laden
    img = cv2.imread(image_path)

    # Für die Anzeige in Matplotlib (RGB-Format) konvertieren
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Vorhersage ermitteln
    prediction_text = predict_defect(image_path)

    # Plot erstellen
    plt.imshow(img_rgb)
    plt.title(prediction_text)
    plt.axis('off')  # Achsen ausblenden
    plt.show()


if __name__ == "__main__":
    # Beispielhafter Pfad zu einem Testbild
    # Bitte hier einen echten Dateinamen (z.B. "test.jpg") verwenden
    test_image_path = 'test.jpg'  # oder 'test.png'

    # Bild anzeigen und Vorhersage in der Titelzeile ausgeben
    show_image_with_prediction(test_image_path)