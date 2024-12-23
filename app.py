import os
import time
import streamlit as st

# Eigene Module
import config
from transformations import canny_edge_detection
import camera
from schrittmotor_TB6600 import StepperMotor

# Globale Konstante oder aus config-Datei
OUTPUT_DIRECTORY = config.output_directory

# Streamlit-Titel
st.title('Image Analysis')

# Tabs in Streamlit
tab1, tab2, tab3 = st.tabs(["Image Capture", "Edge Detection", "AI"])

######################################
# TAB 1: Image Capture
######################################
with tab1:
    st.write("## Test Image")
    
    # Button zum Aufnehmen eines einzelnen Testbildes
    if st.button("Make Test Image"):
        cam = camera.Camera()
        # Speicherpfad für das Testbild
        cam.set_file_path("./test_images")
        # Ein eindeutiger Dateiname basierend auf Zeitstempel
        cam.set_file_name(f"{int(time.time())}_captured_image.CR2")

        # Bild aufnehmen
        test_image = cam.capture_image()

        # Bild anzeigen, falls vorhanden
        if test_image is not None and os.path.isfile(test_image):
            st.image(test_image)
        else:
            st.write("No test image found or file could not be loaded!")

    # Abschnitt "Image Series"
    st.write("## Image Series")

    # Eingabe der Anzahl der aufzunehmenden Bilder
    number_of_images = st.number_input("Number of Images to Capture", 1, 10, 1)

    # Textfeld für Ordnernamen
    name = st.text_input("Name for the Folder", value="default_folder")

    # Freies Textfeld für Kommentare
    comments = st.text_area("Comments")

    # Button zum Starten der Bilderfassung
    if st.button("Capture Images!"):
        # Kamera-Objekt instanzieren
        cam = camera.Camera()

        # Motor loslassen (falls zuvor aktiviert)
        StepperMotor.release()

        # Neues StepperMotor-Objekt erzeugen und Richtung festlegen
        stepper = StepperMotor()
        stepper.set_direction('left')  # z.B. links herum

        # Schrittgröße in Grad berechnen (volle 360° / Anzahl Bilder)
        degree_step = 360 / number_of_images
        current_degree = 0

        # Ordner für die Bilderserie anlegen
        image_folder = f"./captured_images/{name}"
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        # Für jede Position ein Bild aufnehmen
        for _ in range(number_of_images):
            # Motor um den berechneten Winkel bewegen
            stepper.move_by_degree(degree_step)
            current_degree += degree_step

            # Kurze Wartezeit, damit der Motor sich stabilisiert
            time.sleep(0.5)

            # Kamera-Dateiname (mit aktuellem Zeitstempel + Gradzahl)
            cam.set_file_path(image_folder)
            cam.set_file_name(f"{int(time.time())}_{int(current_degree)}_captured_image.CR2")

            captured_image = cam.capture_image()

            if captured_image is not None and os.path.isfile(captured_image):
                st.write(f"## Image Captured at {current_degree:.2f} degrees")
                st.image(captured_image)
            else:
                st.write(f"Could not load the image at {current_degree:.2f} degrees")

        # Liste der aufgenommenen Bilder anzeigen
        st.write("## Captured Images")
        images = [f.name for f in os.scandir(image_folder) if f.is_file()]
        st.write(images)

        # Motor wieder ausschalten
        stepper.disable_motor()

    # Steuerungs-Optionen für den Motor
    st.write("## Motor Options")
    
    degree_input = st.number_input("Turn Motor by degree", value=0)

    if st.button("Turn motor by degree!"):
        # Sicherstellen, dass 'stepper' existiert
        try:
            stepper.move_by_degree(int(degree_input))
        except NameError:
            st.write("Stepper motor is not initialized! Please capture an image series first.")

    # Motor in die Ausgangsposition zurückfahren
    if st.button("Bring back to original position"):
        try:
            stepper.move_to_original_position()
        except NameError:
            st.write("Stepper motor is not initialized! Please capture an image series first.")


######################################
# TAB 2: Edge Detection
######################################
with tab2:
    # Aufteilung in zwei Spalten (links: Original, rechts: Parameter)
    col1, col2 = st.columns(2)

    with col1:
        st.write("## Original Image")
        # Anzeige aller Unterordner in OUTPUT_DIRECTORY
        subfolders = [f.name for f in os.scandir(OUTPUT_DIRECTORY) if f.is_dir()]

        # Dropdown zur Auswahl eines Unterordners
        selected_subfolder = st.selectbox("Select a subfolder", subfolders)

        # Bilddateien im gewählten Unterordner
        images_in_subfolder = [
            f.name for f in os.scandir(os.path.join(OUTPUT_DIRECTORY, selected_subfolder))
            if f.is_file()
        ]

        # Dropdown zur Auswahl eines Bildes
        selected_image = st.selectbox("Select an image", images_in_subfolder)

    with col2:
        st.write("## Select Parameters")

        # Schieberegler für Canny-Parameter
        low_threshold = st.slider("Low Threshold", 0, 255, 150)
        high_threshold = st.slider("High Threshold", 0, 255, 160)
        aperture_size = st.slider("Aperture Size", 3, 7, 3, step=2)

        transformed_image = None
        try:
            # Kompletter Pfad zum ausgewählten Bild
            full_image_path = os.path.join(OUTPUT_DIRECTORY, selected_subfolder, selected_image)
            transformed_image = canny_edge_detection(
                full_image_path, 
                low_threshold, 
                high_threshold, 
                aperture_size
            )
        except FileNotFoundError:
            st.write("The selected file was not found.")
        except Exception as e:
            st.write(f"An error occurred: {e}")

    # Anzeige der Original- und transformierten Bilder in zwei Spalten
    col3, col4 = st.columns(2)

    with col3:
        st.write("### Original")
        original_path = os.path.join(OUTPUT_DIRECTORY, selected_subfolder, selected_image)
        if selected_image and os.path.isfile(original_path):
            st.image(original_path)
        else:
            st.write("No valid image selected.")

    with col4:
        st.write("### Edge Detection Result")
        if transformed_image is not None:
            st.image(transformed_image)
        else:
            st.write("No transformed image available.")


######################################
# TAB 3: AI
######################################
with tab3:
    st.write("## Coming Soon")
    st.write("Hier könnten zukünftig KI-Funktionen eingebunden werden.")