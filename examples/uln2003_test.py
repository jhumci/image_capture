#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# ---------------------------------------------------------
# Hardware-Pins (BCM-Nummerierung)
# ---------------------------------------------------------
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# ---------------------------------------------------------
# Parameter für den Schrittmotor
# ---------------------------------------------------------
# Zwischenzeit zwischen zwei Schritten (Je kleiner, desto schneller)
STEP_SLEEP = 0.002

# 5.625 * (1/64) pro Schritt => 4096 Schritte = 360°
STEP_COUNT = 4096

# Drehrichtung (True = Uhrzeigersinn / clockwise, False = Gegenuhrzeigersinn / counter-clockwise)
direction = False

# Schrittmuster (Halbschrittmodus), Quelle siehe Dokumentation
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
# Setup
# ---------------------------------------------------------
GPIO.setmode(GPIO.BCM)

# Setze die vier Pins als Ausgänge
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Initialisiere die Pins auf LOW
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)

# Pins in einer Liste, um sie in der Loop iterieren zu können
motor_pins = [IN1, IN2, IN3, IN4]

# Merker für den aktuellen Index in der STEP_SEQUENCE
motor_step_counter = 0


def cleanup():
    """
    Setzt alle Motor-Pins auf LOW und säubert die GPIO-Einstellungen.
    Sollte immer am Ende des Skripts oder bei einem Abbruch aufgerufen werden,
    damit der Motor nicht in einem undefinierten Zustand verbleibt.
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
    # Eine volle Umdrehung (STEP_COUNT Schritte)
    for i in range(STEP_COUNT):
        # Schrittmuster auf die GPIO-Pins legen
        for pin_idx in range(len(motor_pins)):
            GPIO.output(motor_pins[pin_idx], STEP_SEQUENCE[motor_step_counter][pin_idx])
        
        # Drehrichtung auswerten und motor_step_counter anpassen
        if direction is True:
            # Uhrzeigersinn
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction is False:
            # Gegenuhrzeigersinn
            motor_step_counter = (motor_step_counter + 1) % 8
        else:
            # Defensive Programmierung
            print("Uh oh... direction sollte immer True oder False sein.")
            cleanup()
            exit(1)
        
        # Kurze Pause zwischen Schritten
        time.sleep(STEP_SLEEP)

# Wenn der User das Skript mit STRG + C abbricht, alles aufräumen
except KeyboardInterrupt:
    cleanup()
    exit(1)

# Nach der Schleife sauber alles aufräumen
cleanup()
exit(0)