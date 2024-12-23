import subprocess
import os
import time


class Camera:
    """
    Klasse für die Steuerung einer Kamera (Canon EOS 70D) über gphoto2.
    """

    def __init__(self):
        """
        Beim Instanzieren wird direkt geprüft, ob eine Canon EOS 70D
        via gphoto2 erkannt wird. Gibt eine Meldung aus, wenn die
        Kamera nicht gefunden wird.
        """
        try:
            # --auto-detect ermittelt automatisch verbundene Kameras
            result = subprocess.run(
                ["gphoto2", "--auto-detect"],
                capture_output=True,
                text=True
            )
            
            # Prüfen, ob 'Canon EOS 70D' im Ausgabe-String enthalten ist
            if "Canon EOS 70D" in result.stdout:
                print("Kamera erfolgreich verbunden!")
            else:
                print("Kamera nicht gefunden. Bitte überprüfen Sie die Verbindung.")
        
        except FileNotFoundError:
            # Wenn gphoto2 nicht installiert ist oder nicht im PATH
            print("gphoto2 ist nicht installiert oder im Systempfad nicht verfügbar.")
        except Exception as e:
            print(f"Fehler bei der Überprüfung der Kamera-Verbindung: {e}")

    def set_file_name(self, file_name):
        """
        Setzt den Dateinamen für das aufgenommene Bild.
        
        Parameter:
        -----------
        file_name : str
            Gewünschter Dateiname, z. B. "bild.CR2"
        """
        self.file_name = file_name

    def set_file_path(self, file_path):
        """
        Setzt das Zielverzeichnis für das aufgenommene Bild und legt
        das Verzeichnis an, wenn es noch nicht existiert.
        
        Parameter:
        -----------
        file_path : str
            Pfad zum gewünschten Verzeichnis, z. B. "./test_images"
        """
        self.file_path = file_path
        
        # Verzeichnis erstellen, falls nicht vorhanden
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    def capture_image(self):
        """
        Nimmt ein Bild auf und lädt es unter dem zuvor definierten Pfad und Dateinamen herunter.

        Rückgabewert:
        --------------
        str
            Der komplette Pfad zur gespeicherten Bilddatei,
            falls alles erfolgreich lief. None bei Fehlern.
        """
        try:
            # Beende ggf. laufende gphoto2-Prozesse, um Konflikte zu vermeiden
            subprocess.run(["pkill", "-f", "gphoto"])

            # Befehl für Bildaufnahme und automatischen Download
            cmd = [
                "gphoto2", 
                "--capture-image-and-download", 
                "--filename", f"{self.file_path}/{self.file_name}"
            ]

            # Ausführen des Kommandos mit Popen, um Eingaben abzufangen
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Hier geben wir 'y' ein, falls gphoto2 eine Überschreibungsabfrage macht
            stdout, stderr = process.communicate(input='y\n')

            # Optional: Ausgabe von stdout/stderr zur Fehlerdiagnose
            # print("STDOUT:", stdout)
            # print("STDERR:", stderr)

            # Return-Code prüfen, falls gewünscht
            if process.returncode != 0:
                print(f"Fehler beim Aufnehmen des Bildes (Returncode {process.returncode}):\n{stderr}")
                return None

            # Bild wurde erfolgreich gespeichert
            return f"{self.file_path}/{self.file_name}"

        except FileNotFoundError:
            print("gphoto2 ist nicht installiert oder im Systempfad nicht verfügbar.")
            return None
        except Exception as e:
            print(f"Fehler beim Aufnehmen des Bildes: {e}")
            return None


if __name__ == "__main__":
    # Beispielhafter Testaufruf, falls das Skript direkt ausgeführt wird
    cam = Camera()

    # Setze den Pfad und Dateinamen, hier mit Zeitstempel
    output_path = "./test_images"
    filename = f"{int(time.time())}_captured_image.CR2"

    cam.set_file_path(output_path)
    cam.set_file_name(filename)

    saved_file = cam.capture_image()
    if saved_file:
        print(f"Bild erfolgreich gespeichert unter: {saved_file}")
    else:
        print("Fehler bei der Bildaufnahme.")