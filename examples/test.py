import os
import numpy as np
import cv2
from matplotlib import pyplot as plt
from tensorflow.keras.models import load_model

# Parameter zur Bildgrößenanpassung (müssen mit dem Training übereinstimmen)
img_height, img_width = 128, 128

def predict_defect(image_path, model):
    """
    Liest ein Bild ein, passt die Größe an und führt eine Vorhersage
    mit dem geladenen Modell durch.

    Parameter:
    -----------
    image_path : str
        Pfad zum Bild.
    model : tf.keras.Model
        Vorher geladene Keras-Modellinstanz.

    Rückgabewert:
    --------------
    str
        "Defekt erkannt" oder "Kein Defekt erkannt" abhängig vom Klassifikationsergebnis.
    """
    if not os.path.isfile(image_path):
        return f"Bildpfad nicht gefunden: {image_path}"

    # Bild in BGR-Format mit OpenCV laden
    img = cv2.imread(image_path)

    # Auf gewünschte Größe skalieren (muss zum Trainingsprozess passen)
    img = cv2.resize(img, (img_height, img_width))

    # Normalisierung auf [0, 1] 
    img = img / 255.0

    # Batch-Dimension hinzufügen (Keras erwartet [Batch, Höhe, Breite, Kanäle])
    img = np.expand_dims(img, axis=0)

    # Vorhersage durchführen
    prediction = model.predict(img)  # Gibt i.d.R. ein Array der Form [[score]]

    # Da das Modell scheinbar binär klassifiziert, wird bei score > 0.5 ein Defekt angenommen
    if prediction[0][0] > 0.5:
        return "Defekt erkannt"
    else:
        return "Kein Defekt erkannt"


def show_image_with_prediction(image_path, model):
    """
    Zeigt das Bild mithilfe von matplotlib an und setzt den Titel
    je nach Vorhersageergebnis ("Defekt erkannt" / "Kein Defekt erkannt").
    """
    if not os.path.isfile(image_path):
        print(f"Kann Bild nicht laden, Pfad existiert nicht: {image_path}")
        return

    # Bild mit OpenCV laden (BGR) und für matplotlib zu RGB konvertieren
    img_bgr = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # Vorhersage ermitteln
    prediction_text = predict_defect(image_path, model)

    # Plot erstellen
    plt.figure(figsize=(6, 6))  # Optional: Größe des angezeigten Bildes
    plt.imshow(img_rgb)
    plt.title(prediction_text)
    plt.axis('off')  # Achsen ausblenden
    plt.show()


if __name__ == "__main__":
    # 1. Modell laden
    model_path = 'defect_detection_model.h5'
    
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Das Modell '{model_path}' wurde nicht gefunden.")
    
    model = load_model(model_path)
    print(f"Modell '{model_path}' erfolgreich geladen.")

    # 2. Verzeichnis der Bilder definieren
    image_directory = "test.bilder"

    # Prüfen, ob das Verzeichnis existiert
    if not os.path.isdir(image_directory):
        raise NotADirectoryError(f"Das Verzeichnis '{image_directory}' wurde nicht gefunden.")

    # 3. Liste der zu klassifizierenden Bilddateien
    image_files = [
        "images.jpeg",
        "images (1).jpeg",
        "images (2).jpeg",
        "images (3).jpeg",
        "Download (1).jpeg",
        "Download (2).jpeg"
    ]

    # 4. Vorhersagen für jedes Bild anzeigen
    for image_file in image_files:
        image_path = os.path.join(image_directory, image_file)
        show_image_with_prediction(image_path, model)