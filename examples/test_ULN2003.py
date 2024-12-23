import RPi.GPIO as GPIO
import time

# ---------------------------------------------------------
# Hardware-Pins (BCM-Nummerierung)
# ---------------------------------------------------------
IN1 = 17  # An IN1 des ULN2003 / Stepper
IN2 = 18  # An IN2
IN3 = 27  # An IN3
IN4 = 22  # An IN4

# ---------------------------------------------------------
# Einstellungen zum Schrittmotor
# ---------------------------------------------------------
# Schlafzeit zwischen zwei Steps (Je kleiner, desto schneller, aber nicht zu klein wählen)
STEP_SLEEP = 0.002

# 5.625*(1/64) pro Schritt = 4096 Schritte für eine 360°-Drehung
STEP_COUNT = 4096

# Drehrichtung (True = im Uhrzeigersinn / clockwise, False = gegen den Uhrzeigersinn / counter-clockwise)
direction = False

# Schrittmuster (Sequenz der GPIO-Ausgänge)
# Dies ist die Halbschrittsequenz für den 28BYJ-48 (8 Schritte pro Zyklus).
STEP_SEQUENCE = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

# ---------------------------------------------------------
# GPIO-Setup
# ---------------------------------------------------------
GPIO.setmode(GPIO.BCM)  # BCM-Nummerierung verwenden
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Pins erstmal auf LOW setzen
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)

motor_pins = [IN1, IN2, IN3, IN4]
motor_step_counter = 0  # Hilfsvariable zum Durchlaufen der STEP_SEQUENCE


def cleanup():
    """
    Schaltet alle Motor-Pins auf LOW und gibt die GPIO-Ressourcen frei.
    Diese Funktion sollte am Ende immer aufgerufen werden,
    damit der Motor nicht in einem undefinierten Zustand bleibt.
    """
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    GPIO.cleanup()


# ---------------------------------------------------------
# Hauptprogramm
# ---------------------------------------------------------
try:
    # Beispiel: Eine volle Umdrehung (STEP_COUNT Schritte)
    for i in range(STEP_COUNT):
        # STEP_SEQUENCE hat 8 Einträge, die nacheinander auf die 4 Pins gelegt werden.
        for pin in range(len(motor_pins)):
            GPIO.output(motor_pins[pin], STEP_SEQUENCE[motor_step_counter][pin])

        # Drehrichtung auswerten und motor_step_counter anpassen
        if direction:
            # Uhrzeigersinn
            motor_step_counter = (motor_step_counter - 1) % 8
        else:
            # Gegenuhrzeigersinn
            motor_step_counter = (motor_step_counter + 1) % 8

        # Kurze Pause zwischen den Schritten
        time.sleep(STEP_SLEEP)

except KeyboardInterrupt:
    # Wenn der User das Skript mit STRG+C abbricht, alles aufräumen.
    print("Abbruch vom Benutzer erkannt. GPIO wird zurückgesetzt.")
    cleanup()
    exit(1)

# Nach Ablauf der for-Schleife einmal säubern
cleanup()
exit(0)