import subprocess
import os
import time

class Camera:

    def __init__(self):
        try:
            result = subprocess.run(["gphoto2", "--auto-detect"], capture_output=True, text=True)
            if "Canon EOS 70D" in result.stdout:
                print("Kamera erfolgreich verbunden!")
            else:
                print("Kamera nicht gefunden. Bitte überprüfen Sie die Verbindung.")
        except Exception as e:
            print(f"Fehler bei der Überprüfung der Kamera-Verbindung: {e}")

    def set_file_name(self, file_name):
        self.file_name = file_name

    def set_file_path(self, file_path):
        self.file_path = file_path
        # create directory if not exists
        if not os.path.exists(file_path):
            os.makedirs(file_path)


    def capture_image(self):
        try:

            cmd = ["gphoto2", "--capture-image-and-download", "--filename", f"{self.file_path}/{self.file_name}"]

            # Use Popen to capture and automatically provide input
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input='y\n')
            
            # Provide 'y' as input to automatically overwrite the file
            return f"{self.file_path}/{self.file_name}"
            
        except Exception as e:
            print(f"Fehler beim Aufnehmen des Bildes: {e}")

if __name__ == "__main__":
    cam = Camera()
    cam.set_file_path("./test_images")
    cam.set_file_name(f"{str(int(time.time()))}_captured_image.CR2")
    cam.capture_image()
