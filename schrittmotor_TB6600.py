#!/usr/bin/python3
import lgpio
import time

class StepperMotor:

    def __init__(self, DIR=20, PUL=21, ENA=16):
        self.handle = lgpio.gpiochip_open(0)  # Öffne den GPIO-Chip 0

        # Raspberry Pi Pin-Belegung für TB6600 Treiber
        self.DIR = DIR
        self.PUL = PUL
        self.ENA = ENA

        self.DIR_Left = 0  # Common-Anode-Konfiguration: 0 aktiviert den Pin
        self.DIR_Right = 1

        self.ENA_Locked = 1
        self.ENA_Released = 0

        self.claim_output(self.DIR)
        self.claim_output(self.PUL)
        self.claim_output(self.ENA)

    def claim_output(self, pin):
        try:
            lgpio.gpio_claim_output(self.handle, pin)
        except lgpio.error:
            lgpio.gpiochip_close(self.handle)
            self.handle = lgpio.gpiochip_open(0)
            lgpio.gpio_claim_output(self.handle, pin)

    def enable_motor(self):
        lgpio.gpio_write(self.handle, self.ENA, self.ENA_Locked)

    def disable_motor(self):
        lgpio.gpio_write(self.handle, self.ENA, self.ENA_Released)

    def set_direction(self, direction):
        if direction == 'left':
            lgpio.gpio_write(self.handle, self.DIR, self.DIR_Left)
        else:
            lgpio.gpio_write(self.handle, self.DIR, self.DIR_Right)

    def move(self, steps):
        for _ in range(steps):
            lgpio.gpio_write(self.handle, self.PUL, 0)  # Common-Anode: 0 aktiviert den Pin
            time.sleep(0.001)  # Pulsweite anpassen
            lgpio.gpio_write(self.handle, self.PUL, 1)  # Common-Anode: 1 deaktiviert den Pin
            time.sleep(0.001)  # Pulsweite anpassen

    def move_by_degree(self, degree):
        steps_per_revolution = 200  # Schritte pro Umdrehung (abhängig vom Motor)
        steps = int(steps_per_revolution * (degree / 360.0))
        self.move(steps)

    def close(self):
        lgpio.gpiochip_close(self.handle)

if __name__ == "__main__":
    stepper = StepperMotor(DIR=20, PUL=21, ENA=16)
    stepper.enable_motor()
    stepper.set_direction('left')
    stepper.move_by_degree(90)
    stepper.disable_motor()
    stepper.close()
