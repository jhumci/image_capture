import gpiod
import time

# 1) Öffne den Chip (z. B. "gpiochip0")
#    Auf vielen Systemen (insbesondere Raspberry Pi) ist /dev/gpiochip0 
#    der erste Chip, der die meisten GPIO-Pins abbildet.
chip = gpiod.Chip('gpiochip0')

# 2) Hole eine bestimmte Linie (Pin), hier Offset 12
#    (Achtung: Das ist nicht zwingend BCM12, sondern "Offset 12" im Chip gpiochip0).
line = chip.get_line(12)

# 3) Konfiguriere die Linie als Eingang, mit internem Pull-Up-Widerstand
#    -> gpiod.LINE_REQ_FLAG_BIAS_PULL_UP bedeutet, dass der Pin auf HIGH gezogen wird, 
#       solange kein externer Schalter ihn auf LOW zieht.
line.request(
    consumer="switch",
    type=gpiod.LINE_REQ_DIR_IN,
    flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP
)

try:
    while True:
        # 4) Lese den Zustand der Linie
        #    - get_value() liefert 1 (HIGH), wenn der Schalter "offen" ist 
        #      (kein Kontakt gegen Masse).
        #    - 0 (LOW), wenn der Schalter geschlossen ist (gegen Masse).
        value = line.get_value()
        
        if value == 0:
            print("Schalter ist geschlossen (LOW)")
        else:
            print("Schalter ist geöffnet (HIGH)")
        
        # 5) Warte ein wenig, um die Ausgabe zu begrenzen
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Programm beendet")

finally:
    # 6) Schließe den Chip/Line, damit andere Prozesse darauf zugreifen können.
    line.release()
    chip.close()