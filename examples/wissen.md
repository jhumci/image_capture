
# Erkennung von Oberflächendefekten auf Metalloberflächen
 ---
# Einführung
## Zielsetzung

Das Hauptziel dieses Projekts ist die Erkennung und Analyse kleiner Kratzer auf metallischen Oberflächen. Solche Defekte können die Funktionalität und das ästhetische Erscheinungsbild von metallischen Bauteilen erheblich beeinträchtigen. Daher ist es wichtig, effiziente Methoden zur automatisierten Erkennung dieser Defekte zu entwickeln und zu implementieren.

## Hintergrund

Oberflächendefekterkennung ist ein weit verbreitetes Problem in der industriellen Fertigung, da selbst kleinste Kratzer oder Unebenheiten die Qualität und Lebensdauer von Produkten beeinflussen können. Traditionelle Methoden zur Inspektion beinhalten manuelle Überprüfungen, die zeitaufwendig und fehleranfällig sind. Moderne Ansätze setzen auf automatisierte Bildverarbeitung und maschinelles Lernen, um Defekte präzise und effizient zu erkennen.

## Methodenübersicht

Für die Erkennung von Oberflächendefekten gibt es verschiedene Ansätze, die in diesem Projekt untersucht und angewendet werden sollen:

1. **Traditionelle Bildverarbeitungsalgorithmen:**
   - **Kantendetektion:** Verwendung von Algorithmen wie Canny Edge Detection, um Kanten im Bild zu identifizieren, die auf Kratzer hinweisen könnten.
   - **Histogrammanalyse:** Analyse der Helligkeitsverteilung im Bild, um Anomalien zu entdecken.
   - **Morphologische Operationen:** Nutzung von Erosion und Dilatation, um Strukturen im Bild zu manipulieren und Defekte zu isolieren.
  
2. **Moderne Ansätze mit künstlicher Intelligenz:**
   - **Convolutional Neural Networks (CNNs):** Einsatz von CNNs zur automatischen Erkennung von Defekten durch Training auf großen Datensätzen.
   - **Transfer Learning:** Verwendung vortrainierter Modelle, die an spezifische Defekttypen angepasst werden können.
   - **Realtime-Erkennung:** Anwendung von Modellen wie YOLO (You Only Look Once) für die Echtzeiterkennung von Defekten.

## Technische Spezifikationen

Um optimale Ergebnisse zu erzielen, müssen die Kamera- und Beleuchtungseinstellungen sorgfältig ausgewählt werden:

- **Kamera-Winkel:** Typischerweise zwischen 0 und 45 Grad zur Oberfläche.
- **Licht-Winkel:** Verwendung von Schräglicht (30-60 Grad), um Defekte hervorzuheben.
- **Brennweite:** Makroobjektive (50mm bis 100mm) für hohe Detailtreue.
- **Belichtungszeit:** Kurze Belichtungszeiten (z.B. 1/1000s) zur Vermeidung von Bewegungsunschärfe.
- **ISO:** Niedrige ISO-Werte (ISO 100-200) zur Minimierung von Rauschen.

## Literaturübersicht

Im Rahmen der Recherche wurden verschiedene wissenschaftliche Quellen untersucht, die die Methoden zur Oberflächendefekterkennung detailliert beschreiben:

1. **Artikel: [What is Surface Defect Detection?](https://medium.com/@saiwa.dotai/what-is-surface-defect-detection-627c711d6439)**
   - **Inhalt:** Überblick über traditionelle Bildverarbeitungsansätze und moderne KI-basierte Methoden.
   - **Ansätze:** Kantendetektion, Histogrammanalyse, CNNs, SVMs.
   - **Kamera- und Licht-Winkel:** 0 bis 45 Grad, Schräglicht.
   - **Technische Spezifikationen:** Makroobjektive, niedrige ISO-Werte, kurze Belichtungszeiten.
![](https://miro.medium.com/v2/resize:fit:750/format:webp/1*UQsDnn0RPHj8ly6iFA4AXw.jpeg){width=50%} ![](https://miro.medium.com/v2/resize:fit:750/format:webp/1*WxXc9GAljR-4Zg-nR9pONQ.jpeg){width=50%}

2. **Paper: [MDPI](https://www.mdpi.com/1424-8220/23/16/7291)**
   
![](https://www.mdpi.com/sensors/sensors-23-07291/article_deploy/html/images/sensors-23-07291-g001-550.jpg){width=50%}
   - **Inhalt:** Untersuchung verschiedener Techniken zur Oberflächendefekterkennung.
   - **Ansätze:** Morphologische Operationen, GLCM, YOLO, Transfer Learning.
   - **Kamera- und Licht-Winkel:** 30-60 Grad, Streiflicht.
   - **Technische Spezifikationen:** 50mm bis 100mm Objektive, kurze Belichtungszeiten, niedrige ISO-Werte.

3. **Video: [YouTube Video on Surface Defect Detection](https://youtu.be/w1Gw6k-8h3Y?si=APDXQnz37om8LtJs)**
<a href="http://www.youtube.com/watch?feature=player_embedded&v=https://youtu.be/w1Gw6k-8h3Y?si=APDXQnz37om8LtJs" target="_blank"><img src="http://img.youtube.com/vi/w1Gw6k-8h3Y/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>
   - **Inhalt:** Praktische Demonstrationen und Anwendung von OpenCV zur Oberflächendefekterkennung.
   - **Ansätze:** OpenCV, ringförmige Beleuchtung.

   - **Inhalt:** Praktische Demonstrationen und Anwendung von OpenCV zur Echtzeiterkennung.
   - **Ansätze:** OpenCV, ringförmige Beleuchtung.
   - **Technische Spezifikationen:** Standardobjektive (35mm-70mm), angepasste Belichtungszeit und ISO.

1. **Artikel: [A Comprehensive Review on Surface Defect Detection Using Image Processing Techniques](https://www.sciencedirect.com/science/article/pii/S0926580523004466)**
   
![](https://ars.els-cdn.com/content/image/1-s2.0-S0926580523004466-gr6.jpg)
   - **Inhalt:** Umfassende Übersicht über Bildverarbeitungstechniken zur Defekterkennung.
   - **Ansätze:** Verschiedene Bildverarbeitungsalgorithmen, maschinelles Lernen.
   - **Kamera- und Licht-Winkel:** Variiert je nach Methode.
   - **Technische Spezifikationen:** Abhängig von der spezifischen Methode.

5. **Buch: [Computer Vision for Industrial Defect Inspection](https://www.mrforum.com/product/9781644902417-46/)**
   - **Inhalt:** Methoden und Anwendungen der Computer Vision in der industriellen Defektinspektion.
   - **Ansätze:** Verschiedene Computer Vision-Techniken.
   - **Kamera- und Licht-Winkel:** Abhängig von der Anwendung.
   - **Technische Spezifikationen:** Unterschiedlich je nach Anwendungsfall.

6. **Artikel: [Deep Learning Approaches for Surface Defect Detection in Manufacturing](https://www.sciencedirect.com/science/article/abs/pii/S0957417423009740)**
   ![](https://ars.els-cdn.com/content/image/1-s2.0-S0957417423009740-gr1.jpg)
   - **Inhalt:** Untersuchung der neuesten Deep Learning-Methoden zur Defekterkennung.
   - **Ansätze:** Verschiedene Deep Learning-Techniken.
   - **Kamera- und Licht-Winkel:** Abhängig von der spezifischen Methode.
   - **Technische Spezifikationen:** Unterschiedlich je nach Methode.

7. **Artikel: [Defect Detection with Computer Vision in Industrial Automation](https://i-mas.com/en/defect-detection-with-computer-vision-in-industrial-automation/#:~:text=Defect%20detection%20with%20artificial%20vision,products%20on%20the%20production%20line.)**
![](https://i-mas.com/wp-content/uploads/MicrosoftTeams-image-26-768x480.jpg)
   - **Inhalt:** Anwendung von maschinellem Lernen zur automatischen Defekterkennung.
   - **Ansätze:** Maschinelles Lernen, Bildverarbeitungsalgorithmen.
   - **Kamera- und Licht-Winkel:** Variiert je nach Methode.
   - **Technische Spezifikationen:** Unterschiedlich je nach Anwendungsfall.

8. **Artikel: [Detection of Surface Defects with Deep Learning](https://www.evt-web.com/applications/detection-of-surface-defects-with-deep-learning/)**
![](https://www.evt-web.com/wp-content/uploads/2021/06/sample6.jpg){width=50%}
![](https://www.evt-web.com/wp-content/uploads/2021/06/Homogenitaets-Inspektor-1.jpg){width=50%}
![](https://www.evt-web.com/wp-content/uploads/2021/06/sample5.jpg){width=50%}
   - **Inhalt:** Anwendung von Deep Learning zur Erkennung von Oberflächendefekten.
   - **Ansätze:** Deep Learning, Computer Vision.
   - **Kamera- und Licht-Winkel:** Variiert je nach Methode.
   - **Technische Spezifikationen:** Unterschiedlich je nach Anwendungsfall.

9.  **Artikel: [Deep Learning Surface Defect Inspection Quality Control](https://www.tekniker.es/en/deep-learning-surface-defect-inspection-quality-control)**
   - **Inhalt:** Methoden der Qualitätskontrolle durch Deep Learning zur Oberflächendefekterkennung.
   - **Ansätze:** Deep Learning, maschinelles Lernen.
   - **Kamera- und Licht-Winkel:** Variiert je nach Methode.
   - **Technische Spezifikationen:** Unterschiedlich je nach Anwendungsfall.

### Weitere Papiere und Quellen

Um detailliertere Informationen zu finden, wurden zusätzliche Forschungspapiere und Ressourcen durchsucht. Hier sind einige relevante Quellen:

- **Artikel:** "A Comprehensive Review on Surface Defect Detection Using Image Processing Techniques" - bietet eine umfassende Übersicht über die verschiedenen Bildverarbeitungstechniken zur Defekterkennung.
- **Buch:** "Computer Vision for Industrial Defect Inspection" - beschreibt verschiedene Methoden und Anwendungen der Computer Vision in der industriellen Defektinspektion.
- **Konferenzbeiträge:** "Deep Learning Approaches for Surface Defect Detection in Manufacturing" - untersucht die neuesten Deep Learning-Methoden zur Defekterkennung.
- **Artikel:** "Automatic Detection of Surface Defects Using Machine Learning" - beschreibt die Anwendung von maschinellem Lernen zur automatischen Defekterkennung.

### Vertiefte Analyse und Detaillierte Informationen

**Quelle 1: [What is Surface Defect Detection?](https://medium.com/@saiwa.dotai/what-is-surface-defect-detection-627c711d6439)**

- **Bilder und Diagramme:** Leider enthält der Artikel keine direkten Bilder oder Diagramme, die spezifisch für die Oberflächendefekterkennung verwendet werden.
- **Zusätzliche Details:**
  - **Kantendetektion:** Der Canny-Algorithmus ist ein weit verbreiteter Kantendetektionsalgorithmus, der durch Rauschunterdrückung, Gradientenberechnung, nicht-maximale Unterdrückung und Doppelschwellenwerttechnik arbeitet.
  - **Histogrammanalyse:** Histogram Equalization kann verwendet werden, um den Kontrast in Bildern zu verbessern und dadurch Defekte hervorzuheben.
  - **CNNs:** CNNs können durch Training auf großen Datensätzen von Oberflächendefekten spezifische Merkmale lernen und automatisiert Defekte erkennen.

**Quelle 2: [MDPI Paper](https://www.mdpi.com/1424-8220/23/16/7291)**

- **Bilder und Diagramme:**
  - Das Papier enthält Diagramme und Abbildungen zur Illustration der verwendeten Methoden. Hier sind einige relevante Abbildungen:

- **Zusätzliche Details:**
  - **Morphologische Operationen:** Erosion und Dilatation sind Grundoperationen der mathematischen Morphologie. Sie werden verwendet, um Strukturen in Bildern zu manipulieren und Defekte zu isolieren.
  - **GLCM:** Die Grauwert-Kooccurenzmatrix analysiert die Textur eines Bildes, indem sie die Häufigkeit von Pixelpaaren mit bestimmten Grauwerten in einem bestimmten Abstand und Winkel berechnet.

**Quelle 3: [YouTube Video on Surface Defect Detection](https://youtu.be/w1Gw6k-8h3Y?si=APDXQnz37om8LtJs)**

- **Bilder und Diagramme:** Das Video zeigt praktische Beispiele und die Anwendung von OpenCV für die Defekterkennung. Es enthält jedoch keine statischen Bilder, die direkt extrahiert werden können.
- **Zusätzliche Details:**
  - **OpenCV:** Eine weit verbreitete Open-Source-Bibliothek für Bildverarbeitung und Computer Vision. Sie bietet Werkzeuge zur Kanten-, Kontur- und Formenerkennung, die für die Defekterkennung genutzt werden können.

**Quelle 4: [A Comprehensive Review on Surface Defect Detection Using Image Processing Techniques](https://www.sciencedirect.com/science/article/pii/S0167865521002550)**

- **Bilder und Diagramme:** Das Papier enthält mehrere Abbildungen und Diagramme zur Veranschaulichung der verschiedenen Techniken.
- **Zusätzliche Details:**
  - **Bildverarbeitungstechniken:** Der Artikel untersucht verschiedene Bildverarbeitungsalgorithmen und deren Anwendung in der Defekterkennung.
  - **Vergleich der Methoden:** Es wird ein Vergleich zwischen traditionellen und modernen Ansätzen zur Defekterkennung durchgeführt.

**Quelle 5: [Computer Vision for Industrial Defect Inspection](https://link.springer.com/book/10.1007/978-3-030-50847-4)**

- **Bilder und Diagramme:** Das Buch enthält detaillierte Diagramme und Abbildungen zu den beschriebenen Methoden.
- **Zusätzliche Details:**
  - **Computer Vision-Techniken:** Verschiedene Techniken der Computer Vision und deren Anwendung in der industriellen Defektinspektion werden beschrieben.
  - **Praxisbeispiele:** Zahlreiche Praxisbeispiele und Fallstudien verdeutlichen die Anwendung der beschriebenen Methoden.

**Quelle 6: [Deep Learning Approaches for Surface Defect Detection in Manufacturing](https://www.sciencedirect.com/science/article/abs/pii/S0957417423009740)**

- **Bilder und Diagramme:** Der Artikel enthält Diagramme und Abbildungen zu den Deep Learning-Methoden.
- **Zusätzliche Details:**
  - **Deep Learning-Techniken:** Untersuchung der neuesten Deep Learning-Ansätze zur Erkennung von Oberflächendefekten.
  - **Vergleich der Methoden:** Es werden verschiedene Deep Learning-Methoden miteinander verglichen und ihre Effektivität bewertet.

**Quelle 7: [Defect Detection with Computer Vision in Industrial Automation](https://i-mas.com/en/defect-detection-with-computer-vision-in-industrial-automation/#:~:text=Defect%20detection%20with%20artificial%20vision,products%20on%20the%20production%20line.)**

- **Bilder und Diagramme:** Die Webseite enthält Abbildungen zur Veranschaulichung der Defekterkennung in der industriellen Automatisierung.
- **Zusätzliche Details:**
  - **Maschinelles Lernen:** Anwendung von maschinellem Lernen zur automatischen Erkennung von Oberflächendefekten.
  - **Vergleich der Methoden:** Vergleich der Effektivität verschiedener maschineller Lernmethoden zur Defekterkennung.

**Quelle 8: [Detection of Surface Defects with Deep Learning](https://www.evt-web.com/applications/detection-of-surface-defects-with-deep-learning/)**

- **Bilder und Diagramme:** Die Webseite enthält Abbildungen zur Veranschaulichung der Anwendung von Deep Learning zur Defekterkennung.
- **Zusätzliche Details:**
  - **Deep Learning:** Anwendung von Deep Learning zur Erkennung von Oberflächendefekten.
  - **Vergleich der Methoden:** Vergleich der Effektivität verschiedener Deep Learning-Methoden zur Defekterkennung.

**Quelle 9: [Deep Learning Surface Defect Inspection Quality Control](https://www.tekniker.es/en/deep-learning-surface-defect-inspection-quality-control)**

- **Bilder und Diagramme:** Die Webseite enthält Abbildungen zur Veranschaulichung der Qualitätskontrolle durch Deep Learning.
- **Zusätzliche Details:**
  - **Deep Learning:** Methoden der Qualitätskontrolle durch Deep Learning zur Oberflächendefekterkennung.
  - **Vergleich der Methoden:** Vergleich der Effektivität verschiedener Deep Learning-Methoden zur Qualitätskontrolle.

## Zusammenfassung der Ergebnisse

**Ansätze zur Defekterkennung:**

- **Traditionelle Bildverarbeitungsalgorithmen:** Kantendetektion, Histogrammanalyse, morphologische Operationen.
- **KI-Modelle:** CNNs, YOLO, Transfer Learning.

**Kamera- und Licht-Winkel:**

- **Kamera-Winkel:** 0 bis 60 Grad.
- **Licht-Winkel:** 30-60 Grad, Schräglicht und ringförmige Beleuchtung.

**Technische Spezifikationen:**

- **Brennweite:** 35mm bis 100mm, abhängig von der Detailtiefe.
- **Belichtungszeit:** Kurz (1/1000s), um Bewegungsunschärfe zu vermeiden.
- **ISO:** Niedrig (ISO 100-200), um Rauschen zu minimieren.

# Nächste schritte in der Theorie
## 1. Datenaufzeichnung

### Ziel

Überprüfung der Möglichkeit, die Canon EOS 70D direkt vom PC aus zu steuern und Bilder aufzunehmen.

### Wichtige Überlegungen beim Bildermachen

- **Auflösung:** Hohe Auflösung, um feine Details und kleine Kratzer sichtbar zu machen.
- **Beleuchtung:** Verwendung von Schräglicht (30-60 Grad) oder Streiflicht, um Defekte hervorzuheben. Vermeide direkte Reflexionen.
- **Fokus und Stabilität:** Verwende ein Stativ oder eine stabile Halterung, um Bewegungsunschärfe zu vermeiden und sicherzustellen, dass die Kamera korrekt fokussiert ist.
- **Belichtung:** Stelle sicher, dass die Bilder gut beleuchtet sind, ohne Über- oder Unterbelichtung. Verwende niedrige ISO-Werte (ISO 100-200), um Rauschen zu minimieren.

### Vorgehen

1. **Installation von gPhoto2:** Ein Tool zur Steuerung der Kamera über die Kommandozeile.
2. **Python-Skript zur Steuerung der Kamera:** Ein Skript, das gPhoto2 verwendet, um Bilder aufzunehmen und auf dem Computer zu speichern.

### Installation der benötigten Pakete unter Windows

#### Installiere gPhoto2

gPhoto2 kann unter Windows über das WSL (Windows Subsystem for Linux) installiert werden. Folge den Anweisungen zur Installation von WSL und Ubuntu auf Windows: [Installieren des WSL](https://docs.microsoft.com/de-de/windows/wsl/install).

Nach der Installation von WSL und Ubuntu
```bash
sudo apt-get update
sudo apt-get install gphoto2
```
Installiere Python und die erforderlichen Pakete:

Lade und installiere Python von python.org.
Installiere die benötigten Python-Bibliotheken:
```bash
pip install numpy opencv-python tensorflow matplotlib
```

## 2. Datenvorverarbeitung
### Ziel
Vorbereitung der aufgenommenen Bilder für das Training des Modells, einschließlich Bildskalierung und -augmentation.

### Vorgehen
- Bildskalierung: Anpassung der Bildgröße.
- Bildaugmentation: Erweiterung des Datensatzes durch #zufällige Transformationen.

## 3. Modelltraining
### Ziel
Erstellung und Training eines Convolutional Neural Networks (CNN) zur Erkennung von Defekten in Bildern.

### Vorgehen
- Modellarchitektur: Definition eines CNN-Modells.
- Training: Training des Modells mit den vorbereiteten Daten.
- Validierung: Überprüfung der Modellleistung mit Testdaten

## 4. Fehlererkennung
### Ziel
Verwendung des trainierten Modells zur Erkennung von Defekten in neuen Bildern.

### Vorgehen
- Bildvorhersage: Laden des Modells und Vorhersage, ob ein Bild Defekte enthält.
- Visualisierung: Anzeige des Bildes mit der Vorhersage.

## Zusammenfassung der Schritte
1. **Datenaufzeichnung**: Verwende gPhoto2 und ein Python-Skript, um Bilder mit der Canon EOS 70D aufzunehmen. Achte dabei auf hohe Auflösung, optimale Beleuchtung, korrekten Fokus und Stabilität sowie richtige Belichtung.
2. **Datenvorverarbeitung**: Skaliere und augmentiere die Bilder, um sie für das Training vorzubereiten.
3. **Modelltraining**: Erstelle und trainiere ein CNN-Modell mit den vorbereiteten Daten.
4. **Fehlererkennung**: Verwende das trainierte Modell, um Defekte in neuen Bildern zu erkennen und visualisiere die Ergebnisse.
   
Durch die systematische Durchführung dieser Schritte kann ein robustes System zur Erkennung von Oberflächendefekten auf metallischen Oberflächen entwickelt werden.

## Fazit

Durch die Kombination traditioneller Bildverarbeitungstechniken mit modernen KI-Methoden soll eine robuste Lösung zur Erkennung von Oberflächendefekten auf metallischen Oberflächen entwickelt werden. Dies wird die Effizienz und Genauigkeit der Qualitätskontrolle in der industriellen Fertigung erheblich verbessern.

 ---