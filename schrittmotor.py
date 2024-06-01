# https://www.heimkino-praxis.de/leinwand-maskierung-schrittmotor-steuerung/
import RPi.GPIO as GPIO
import time


class StepperMotor:

    def __init__(self, DIR=33, PUL=35, ENA=37):
        GPIO.setmode(GPIO.BOARD)

        # Raspberry Pi Pin-Belegung für TB6600 Treiber
        self.DIR = 33
        self.PUL = 35
        self.ENA = 37

        self.DIR_Left = GPIO.HIGH
        self.DIR_Right = GPIO.LOW

        self.ENA_Locked = GPIO.LOW
        self.ENA_Released = GPIO.HIGH

        GPIO.setwarnings(False)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(PUL, GPIO.OUT)
        GPIO.setup(ENA, GPIO.OUT)


    # Motor aktivieren und halten
    def enable_motor(self):
        GPIO.output(self.ENA, self.ENA_Locked)

    # Motor freigeben
    def disable_motor(self):
        GPIO.output(self.ENA, self.ENA_Released)

    # Richtung setzen
    def set_direction(self, direction):
        if direction == 'left':
            GPIO.output(self.DIR, self.DIR_Left)
        else:
            GPIO.output(self.DIR, self.DIR_Right)

    # Schritte ausführen

    def move(self, steps):
        for i in range(steps):
            # Puls modulieren
            GPIO.output(self.PUL, GPIO.HIGH)
            time.sleep(0.0001875)

            GPIO.output(self.PUL, GPIO.LOW)
            time.sleep(0.0001875)

    def move_by_degree(self, degree):
        steps = int(degree / 1.8)
        self.move(steps)

if __name__ == "__main__":
    stepper = StepperMotor()
    stepper.enable_motor()
    stepper.set_direction('left')
    stepper.move_by_degree(90)
    stepper.disable_motor()
    GPIO.cleanup()
