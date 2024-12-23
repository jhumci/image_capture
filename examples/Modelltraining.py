from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Beispielhafte Bild-Höhe/Breite und Batch-Größe
# (müssen irgendwo definiert sein oder definiere sie direkt hier)
img_height = 128
img_width = 128
batch_size = 32

# Modellarchitektur
model = Sequential([
    # 1. Convolution + ReLU-Aktivierung
    #   input_shape = (img_height, img_width, 3), da es ein RGB-Bild ist
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D(pool_size=(2, 2)),

    # 2. Convolution + ReLU-Aktivierung
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    # 3. Convolution + ReLU-Aktivierung
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    # 4. Flatten, um die 2D-Feature-Maps in einen 1D-Vektor zu konvertieren
    Flatten(),

    # 5. Vollständig verbundenes Hidden-Layer mit 512 Neuronen
    Dense(512, activation='relu'),

    # 6. Ausgabeschicht mit 1 Neuron + Sigmoid-Aktivierung
    #    --> Für binäre Klassifikation (Defekt / Kein Defekt)
    Dense(1, activation='sigmoid')
])

# Kompilieren des Modells:
# - optimizer: z. B. Adam mit Standard-Lernrate 0.001
# - loss: binary_crossentropy für binäre Klassifikation
# - metrics: ['accuracy'] zur Überwachung der Genauigkeit
model.compile(
    optimizer=Adam(),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Optional: Einige Callback-Funktionen für besseres Training
# - EarlyStopping: stoppt, wenn sich die Validierungsgenauigkeit oder der -verlust nicht mehr verbessert
# - ModelCheckpoint: speichert das Modell in regelmäßigen Abständen
early_stopping = EarlyStopping(patience=3, restore_best_weights=True)
model_checkpoint = ModelCheckpoint('defect_detection_best_model.h5', save_best_only=True)

# Training des Modells
# - train_generator und test_generator stammen in der Regel aus einem ImageDataGenerator.flow_from_directory(...)
# - steps_per_epoch = Anzahl Trainingssamples / Batch-Größe
# - validation_steps = Anzahl Testsamples / Batch-Größe
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=10,  # Ggf. anpassen
    validation_data=test_generator,
    validation_steps=test_generator.samples // batch_size,
    callbacks=[early_stopping, model_checkpoint]
)

# Speichert das zuletzt trainierte Modell als defect_detection_model.h5
model.save('defect_detection_model.h5')