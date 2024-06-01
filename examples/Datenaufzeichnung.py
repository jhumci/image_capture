import subprocess
import os

def check_camera_connection():
    try:
        result = subprocess.run(["gphoto2", "--auto-detect"], capture_output=True, text=True)
        if "Canon EOS 70D" in result.stdout:
            print("Kamera erfolgreich verbunden!")
        else:
            print("Kamera nicht gefunden. Bitte überprüfen Sie die Verbindung.")
    except Exception as e:
        print(f"Fehler bei der Überprüfung der Kamera-Verbindung: {e}")

def capture_image(output_dir):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        result = subprocess.run(["gphoto2", "--capture-image-and-download", "--filename", f"{output_dir}/captured_image.jpg"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Bild erfolgreich aufgenommen und heruntergeladen!")
        else:
            print(f"Fehler beim Aufnehmen des Bildes: {result.stderr}")
    except Exception as e:
        print(f"Fehler beim Aufnehmen des Bildes: {e}")

if __name__ == "__main__":
    output_directory = "./captured_images"
    check_camera_connection()
    capture_image(output_directory)