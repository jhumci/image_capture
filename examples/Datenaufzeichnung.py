import subprocess
import os


def check_camera_connection(camera_name="Canon EOS 70D"):
    """
    Prüft, ob eine bestimmte Kamera (Default: Canon EOS 70D) per gphoto2 erkannt wird.

    Parameter:
    -----------
    camera_name : str
        Name der erwarteten Kamera (Teilstring, der im Output von gphoto2 auftaucht).

    Rückgabewert:
    --------------
    bool
        True, wenn die Kamera gefunden wurde, False sonst.
    """
    try:
        # --auto-detect erkennt automatisch verbundene Kameras
        result = subprocess.run(
            ["gphoto2", "--auto-detect"], 
            capture_output=True, 
            text=True
        )
        
        # Prüfen, ob der Name der erwarteten Kamera im Output enthalten ist
        if camera_name in result.stdout:
            print("Kamera erfolgreich verbunden!")
            return True
        else:
            print("Kamera nicht gefunden. Bitte überprüfen Sie die Verbindung.")
            return False

    except FileNotFoundError:
        # Tritt auf, wenn gphoto2 nicht installiert oder im Pfad nicht gefunden wird
        print("gphoto2 ist nicht installiert oder im System nicht verfügbar.")
        return False
    except Exception as e:
        print(f"Fehler bei der Überprüfung der Kamera-Verbindung: {e}")
        return False


def capture_image(output_dir, filename="captured_image.jpg"):
    """
    Nimmt ein Bild mit der verbundenen Kamera auf und lädt es herunter.

    Parameter:
    -----------
    output_dir : str
        Zielverzeichnis, in dem das Bild gespeichert wird.
    filename   : str
        Name der Zieldatei (Standard: captured_image.jpg).

    Rückgabewert:
    --------------
    str
        Der vollständige Pfad zur aufgenommenen Bilddatei, falls erfolgreich.
        None, wenn ein Fehler aufgetreten ist.
    """
    try:
        # Verzeichnis erstellen, falls nicht vorhanden
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Vollständigen Pfad zusammenbauen
        output_path = os.path.join(output_dir, filename)

        # gphoto2-Command zum Aufnehmen und Herunterladen des Bildes
        result = subprocess.run(
            ["gphoto2", 
             "--capture-image-and-download", 
             "--filename", output_path],
            capture_output=True, 
            text=True
        )

        # Rückgabecode 0 bedeutet, dass gphoto2 erfolgreich ausgeführt wurde
        if result.returncode == 0:
            print(f"Bild erfolgreich aufgenommen und heruntergeladen: {output_path}")
            return output_path
        else:
            print(f"Fehler beim Aufnehmen des Bildes: {result.stderr.strip()}")
            return None

    except FileNotFoundError:
        print("gphoto2 ist nicht installiert oder im System nicht verfügbar.")
        return None
    except Exception as e:
        print(f"Fehler beim Aufnehmen des Bildes: {e}")
        return None


if __name__ == "__main__":
    output_directory = "./captured_images"

    # 1. Kamera-Verbindung prüfen
    camera_found = check_camera_connection()
    if not camera_found:
        # Wenn die Kamera nicht gefunden wurde, kann hier abgebrochen oder ein Hinweis ausgegeben werden
        print("Kamera wurde nicht erkannt. Bitte erneut versuchen.")
    else:
        # 2. Bild aufnehmen und herunterladen
        captured_file = capture_image(output_directory, "test_captured_image.jpg")
        if captured_file:
            print(f"Aufgenommenes Bild liegt unter: {captured_file}")
        else:
            print("Es trat ein Fehler beim Aufnehmen des Bildes auf.")