import gpiod
import time

# Definiere den GPIO-Chip und die Linie (GPIO-Pin)
chip = gpiod.Chip('gpiochip0')  # Verwende 'gpiochip0', das ist der erste GPIO-Chip auf den meisten Raspberry Pi-Boards
line = chip.get_line(12)  # GPIO12 (entsprechend deinem Schalter)

# Konfiguriere die Linie als Eingabe mit Pull-Up-Widerstand
line.request(consumer="switch", type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

try:
    while True:
        # Lese den Zustand des Schalters
        value = line.get_value()
        if value == 0:
            print("Schalter ist geschlossen")
        else:
            print("Schalter ist geöffnet")
        
        # Kurze Pause, um die Ausgabe zu begrenzen
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Programm beendet")
