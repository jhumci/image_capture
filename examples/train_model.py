import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# --------------------------------------------------
# 1) Hyperparameter und Pfade einstellen
# --------------------------------------------------
# Bilddimensionen und Batch-Größe für den Generator
img_height, img_width = 128, 128
batch_size = 32

# Anzahl an Epochen, die das Modell trainiert
epochs = 10

# Verzeichnisse für Trainings- und Testdaten
train_dir = 'data/train'  # Bilder nach Klassen in Unterordnern
test_dir = 'data/test'

# --------------------------------------------------
# 2) Datenvorverarbeitung und Augmentation
# --------------------------------------------------
# Trainingsdatengenerator:
# - rescale: Skalierung der Pixelwerte von [0,255] auf [0,1]
# - shear_range, zoom_range, horizontal_flip: einfache Datenaugmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Testdatengenerator:
# - Nur Skalierung, da man im Test meist keine Augmentation anwendet
test_datagen = ImageDataGenerator(rescale=1./255)

# Erstellen der Generatoren durch Auslesen der Verzeichnisstruktur
# Struktur muss sein: train_dir/class1, train_dir/class2, ...
# class_mode='binary' => Binäre Klassifikation
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)

# --------------------------------------------------
# 3) Modellaufbau
# --------------------------------------------------
# Einfache CNN-Struktur mit mehreren Conv2D- und MaxPooling-Schichten
# Abschließend Flatten => Dense-Schichten => Output (1 Neuron, sigmoid)
model = Sequential([
    # Erste Convolution-Schicht (Filter=32), ReLU-Aktivierung
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D(pool_size=(2, 2)),

    # Zweite Convolution-Schicht (Filter=64)
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    # Dritte Convolution-Schicht (Filter=128)
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    # Umwandeln der 2D-Feature-Maps in einen Vektor
    Flatten(),

    # Vollständig verbundene (Dense) Schicht
    Dense(512, activation='relu'),

    # Ausgabeschicht mit 1 Neuron (Sigmoid) => Binäre Klassifikation
    Dense(1, activation='sigmoid')
])

# Kompilieren des Modells
# - optimizer='adam': gängiger Optimierer
# - loss='binary_crossentropy': für binäre Klassifikation
# - metrics=['accuracy']: Wir messen die Genauigkeit (Accuracy)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# --------------------------------------------------
# 4) Training
# --------------------------------------------------
# steps_per_epoch = Anzahl Trainingssamples / Batch-Größe
# validation_steps = Anzahl Testsamples / Batch-Größe
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    validation_data=test_generator,
    validation_steps=test_generator.samples // batch_size
)

# --------------------------------------------------
# 5) Speichern des Modells
# --------------------------------------------------
# Speichert das trainierte Modell (inkl. Architektur und Gewichten)
model.save('defect_detection_model.h5')
print("Modell wurde erfolgreich gespeichert.")