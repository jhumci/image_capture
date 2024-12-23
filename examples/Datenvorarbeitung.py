from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Bilddimensionen und Batch-Größe definieren
img_height, img_width = 128, 128
batch_size = 32

# Trainings-Daten-Generator mit Datenaugmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,         # Pixelwerte von [0,255] auf [0,1] skalieren
    shear_range=0.2,        # Zufällige affine Transformation (Scherschnitt) mit Maximalwert 0.2
    zoom_range=0.2,         # Zufälliges Zoomen um max. 20%
    horizontal_flip=True     # Zufälliges horizontales Spiegeln
)

# Test/Validierungs-Daten-Generator
# Hier wird in der Regel nur rescale angewendet, 
# da man auf Validierungs- oder Testdaten normalerweise keine Augmentation anwendet.
test_datagen = ImageDataGenerator(
    rescale=1./255          # Pixelwerte von [0,255] auf [0,1] skalieren
)

# Trainingsdaten-Generator, der Bilder aus einem Verzeichnis lädt
# Struktur: ./data/train/<klasse1>/..., ./data/train/<klasse2>/..., etc.
train_generator = train_datagen.flow_from_directory(
    './data/train',              # Pfad zum Trainingsverzeichnis
    target_size=(img_height, img_width),  # Alle Bilder auf diese Größe skalieren
    batch_size=batch_size,                 # Anzahl der Bilder pro Batch
    class_mode='binary'                    # Da wir von einem binären Klassifikationsproblem ausgehen
)

# Testdaten-Generator, analog zur Validierung
test_generator = test_datagen.flow_from_directory(
    './data/test',               # Pfad zum Testverzeichnis
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary'
)