import gpiod
import time

class StepperMotor:

    def __init__(self, chip_name='gpiochip0', DIR=17, PUL=27, ENA=22, SWITCH=12):
        print("Initialisiere GPIO...")
        self.chip = gpiod.Chip(chip_name)
        self.DIR = self.chip.get_line(DIR)
        self.PUL = self.chip.get_line(PUL)
        self.ENA = self.chip.get_line(ENA)
        self.SWITCH = self.chip.get_line(SWITCH)  # Mikroschalter an GPIO 12

        self.DIR_Left = 0
        self.DIR_Right = 1

        self.ENA_Locked = 0
        self.ENA_Released = 1

        # GPIO-Linien als Ausgang setzen
        self.DIR.request(consumer='stepper-motor', type=gpiod.LINE_REQ_DIR_OUT)
        self.PUL.request(consumer='stepper-motor', type=gpiod.LINE_REQ_DIR_OUT)
        self.ENA.request(consumer='stepper-motor', type=gpiod.LINE_REQ_DIR_OUT)

        # Mikroschalter als Eingang mit Pull-Up-Widerstand setzen
        self.SWITCH.request(consumer='stepper-motor', type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

        self.disable_motor()  # Motor standardmäßig deaktivieren

    def enable_motor(self):
        print("Motor wird aktiviert...")
        self.ENA.set_value(self.ENA_Locked)

    def disable_motor(self):
        print("Motor wird deaktiviert...")
        self.ENA.set_value(self.ENA_Released)

    def set_direction(self, direction):
        if direction.lower() == 'left':
            print("Setze Richtung: Links")
            self.DIR.set_value(self.DIR_Left)
        elif direction.lower() == 'right':
            print("Setze Richtung: Rechts")
            self.DIR.set_value(self.DIR_Right)
        else:
            raise ValueError("Richtung muss entweder 'left' oder 'right' sein.")

    def move(self, steps, delay=0.001):
        print(f"Bewege Motor für {steps} Schritte")
        for _ in range(steps):
            if self.SWITCH.get_value() == 0:  # Schalter gedrückt, Motor stoppen
                print("Schalter betätigt! Motor wird gestoppt.")
                break
            self.PUL.set_value(1)
            time.sleep(delay)
            self.PUL.set_value(0)
            time.sleep(delay)

    def move_to_zero_point(self, delay=0.001):
        """
        Bewege den Motor in Richtung 'left' (Nullpunkt), bis der Mikroschalter ausgelöst wird.
        """
        print("Bewege Motor zum Nullpunkt...")
        self.set_direction('left')
        while self.SWITCH.get_value() == 1:  # Bewege den Motor, bis der Schalter betätigt wird (LOW)
            self.PUL.set_value(1)
            time.sleep(delay)
            self.PUL.set_value(0)
            time.sleep(delay)
        print("Nullpunkt erreicht.")

    def move_by_degree(self, degree, delay=0.001, microsteps=8):
        # Schritte berechnen, unter Berücksichtigung des Mikrosteppings
        steps_per_revolution = 200 * microsteps  # 200 Schritte/Umdrehung x Mikrostepping-Faktor
        steps = int((degree / 360) * steps_per_revolution)
        print(f"Bewege um {degree} Grad, was {steps} Schritten entspricht (Mikrostepping: {microsteps})")
        self.move(steps, delay)

    def cleanup(self):
        print("GPIO-Ressourcen werden freigegeben...")
        self.chip.close()

if __name__ == "__main__":
    stepper = StepperMotor()
    stepper.enable_motor()
    stepper.set_direction('left')
    stepper.move_by_degree(90)
    stepper.disable_motor()
    time.sleep(10)
    stepper.move_to_zero_point()
    stepper.cleanup()
