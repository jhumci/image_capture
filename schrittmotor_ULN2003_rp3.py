#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

class StepperMotor:

    def __init__(self, in1=17, in2=18, in3=27, in4=22):
        """
        Initialisiert den 28BYJ-48 Schrittmotor (oder ähnlichen) über ULN2003 mit 4 Ausgängen:
        in1, in2, in3, in4. Über step_sequence wird ein Halbschrittbetrieb realisiert.
        """

        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4

        # Wartezeit zwischen einzelnen Schritten. 
        # Je kleiner, desto schneller dreht der Motor. Zu klein => Schrittverluste möglich.
        self.step_sleep = 0.002

        # 4096 Steps = eine volle Umdrehung bei Halbschrittmodus (28BYJ-48)
        self.step_count = 4096

        # Richtung: True für clockwise (CW), False für counter-clockwise (CCW)
        # Standardwert
        self.direction = False

        # Schrittmuster im Halbschrittmodus (8 Einzelschritte pro Zyklus)
        # Quelle: http://www.4tronix.co.uk/arduino/Stepper-Motors.php
        self.step_sequence = [
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1]
        ]

        # GPIO-Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)

        # Pins initial auf LOW
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

        self.motor_pins = [self.in1, self.in2, self.in3, self.in4]
        self.motor_step_counter = 0

    def enable_motor(self):
        """
        Falls du den Motor „halten“ willst, könntest du hier 
        ggf. etwas programmieren (z. B. die letzte Schrittkonfiguration anlegen).
        Der 28BYJ-48 hat keinen separaten Enable-Pin wie z. B. ein TB6600.
        """
        print("Motor aktivieren: Aktuell ist kein separater ENA-Pin vorgesehen.")
        # Optional: hier könnte man die letzte Schrittkonfiguration setzen,
        # damit der Motor 'gehalten' wird und Drehmoment aufbaut.

    def disable_motor(self):
        """
        Motor freigeben => alle Pins auf LOW (kein Drehmoment).
        Achtung: Hier wird nicht GPIO.cleanup() aufgerufen! 
        Das sollte erst am Ende deines Programms passieren.
        """
        print("Motor wird deaktiviert (alle Pins auf LOW).")
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)
        # NICHT: GPIO.cleanup() (siehe Hinweis)

    def set_direction(self, direction):
        """
        Setzt die Drehrichtung:
          'left'  => False (counter-clockwise)
          'right' => True (clockwise)
        """
        if direction.lower() == 'left':
            self.direction = False
            print("Richtung: links (counter-clockwise).")
        elif direction.lower() == 'right':
            self.direction = True
            print("Richtung: rechts (clockwise).")
        else:
            raise ValueError("Richtung muss 'left' oder 'right' sein.")

    def move(self, steps):
        """
        Führt eine bestimmte Anzahl 'steps' aus. 
        Ein 'step' iteriert durch self.step_sequence und setzt die Ausgänge entsprechend.
        """
        print(f"Bewege den Motor um {steps} Schritte, Richtung: {'CW' if self.direction else 'CCW'}.")
        for _ in range(steps):
            # step_sequence[motor_step_counter] = [1,0,0,1], etc.
            for pin_idx in range(len(self.motor_pins)):
                GPIO.output(
                    self.motor_pins[pin_idx], 
                    self.step_sequence[self.motor_step_counter][pin_idx]
                )

            # Schrittzähler anpassen, je nach direction
            if self.direction:
                self.motor_step_counter = (self.motor_step_counter - 1) % len(self.step_sequence)
            else:
                self.motor_step_counter = (self.motor_step_counter + 1) % len(self.step_sequence)

            # Kleiner Schlaf, damit der Motor Zeit hat, den Schritt auszuführen
            time.sleep(self.step_sleep)

    def move_by_degree(self, degree):
        """
        Bewegt den Motor um den angegebenen Winkel 'degree' in Grad.
        Achtung: 1.8 Grad/Schritt ist ein typischer Wert für bipolare NEMA17,
        NICHT für den 28BYJ-48 (der hat 4096 Steps pro 360°, also 360/4096 ~ 0.088°/Halbschritt).
        
        Wenn du bei 1.8 Grad/Schritt bleibst, bedeutet das:
          steps = degree / 1.8
        Für den 28BYJ-48 (Halbschritt) wäre korrekter:
          steps = (degree / 360) * 4096
        Passe das je nach Motor/Getriebe an.
        """
        # Standardmäßig 1.8° pro Schritt
        steps = int(degree / 1.8)
        print(f"move_by_degree({degree}) => ~ {steps} Schritte (Annahme: 1.8°/Schritt)")
        self.move(steps)

    def cleanup(self):
        """
        Gibt die GPIO-Ressourcen frei. 
        Dies sollte erst ganz am Ende des Programms aufgerufen werden.
        """
        print("GPIO.cleanup() aufrufen. Alle Ressourcen freigegeben.")
        GPIO.cleanup()


if __name__ == "__main__":
    # Beispiel für die Verwendung
    stepper = StepperMotor()
    
    # Motor 'aktivieren' (hat hier keine praktische Wirkung bei 28BYJ-48)
    stepper.enable_motor()
    
    # Richtung setzen
    stepper.set_direction('left')
    
    # 90 Grad gegen den Uhrzeigersinn
    stepper.move_by_degree(90)
    
    # Motor freigeben (kein Drehmoment)
    stepper.disable_motor()

    # Ganz am Ende des Programms die GPIO-Pins bereinigen
    stepper.cleanup()