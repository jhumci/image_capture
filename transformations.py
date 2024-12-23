import cv2
import os
import numpy as np
import config


def canny_edge_detection(fitem, low_threshold, high_threshold, apertureSize=3):
    """
    Führt eine Canny-Kantendetektion auf dem gegebenen Bild aus und speichert das
    Ergebnis im config.output_directory unter dem Namen 'canny_<Dateiname>'.
    Falls das Eingabebild die Endung .CR2 hat, wird es als .jpg gespeichert.

    Parameter:
    -----------
    fitem : str
        Pfad zum Eingabebild.
    low_threshold : int
        Untere Schwelle für die Canny-Detektion.
    high_threshold : int
        Obere Schwelle für die Canny-Detektion.
    apertureSize : int
        Aperture-Größe (3, 5 oder 7) für den Sobel-Operator in Canny.

    Rückgabewert:
    --------------
    edges : np.ndarray
        Das Ergebnisbild (Kanten) als Numpy-Array im Grayscale.
    """
    # Bild einlesen
    image = cv2.imread(fitem)
    if image is None:
        raise FileNotFoundError(f"Bild konnte nicht gelesen werden: {fitem}")

    # In Graustufen konvertieren
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Canny-Kantendetektion
    edges = cv2.Canny(gray, low_threshold, high_threshold, apertureSize=apertureSize)
    
    # Definiere den Ausgabedateinamen, z. B. ./output/canny_Bild.jpg
    base_name = os.path.basename(fitem)  # z. B. "bild.CR2"
    out_name = "canny_" + base_name
    fout = os.path.join(config.output_directory, out_name)

    # Falls .CR2 am Ende, ersetze durch .jpg
    root, ext = os.path.splitext(fout)
    if ext.lower() == ".cr2":
        fout = root + ".jpg"

    # Kantenbild speichern
    cv2.imwrite(fout, edges)
    return edges


if __name__ == "__main__":
    """
    Hauptteil (wenn das Skript direkt ausgeführt wird).
    Beispiel:
      1. Definiere ein Basisverzeichnis 'captured_images'
      2. Nutze ein Unterverzeichnis für die Ausgabe 'captured_images/Output'
      3. Durchlaufe alle Dateien und führe Canny-Kantendetektion durch.
    """
    # Lokal gesetzt – kann aber auch aus config oder CLI-Argumenten stammen.
    path = "captured_images"

    # Input-Verzeichnis
    inputPar = os.path.join(path)
    # Output-Verzeichnis (Unterordner "Output")
    outPar = os.path.join(path, 'Output')
    os.makedirs(outPar, exist_ok=True)

    # Liste aller Dateien im Input-Verzeichnis
    files = os.listdir(inputPar)

    # Schleife: Für jede Datei die Canny-Kantendetektion durchführen
    for file in files:
        fitem = os.path.join(inputPar, file)

        # Bild lesen (als Farb-Bild)
        image = cv2.imread(fitem)
        if image is None:
            print(f"Überspringe ungültige Datei: {fitem}")
            continue

        # In Graustufen konvertieren
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Canny-Kantendetektion mit beispielhaften Parametern
        edges = cv2.Canny(gray, 150, 160, apertureSize=3)

        # (Optional) Hough-Line-Transformation
        """
        lines = cv2.HoughLines(edges, 1.5, np.pi / 180, 200)
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                # Zeichne die Linie auf das Originalbild (im Farbraum BGR)
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        """

        # Definiere den Ausgabedateinamen (z. B. captured_images/Output/filename.jpg)
        fout = os.path.join(outPar, file)

        # Speichere das Canny-Kantenbild (bzw. edges) ab
        cv2.imwrite(fout, edges)
        print(f"Kantenbild gespeichert unter: {fout}")