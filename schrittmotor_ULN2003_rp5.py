#!/usr/bin/python3
import gpiod
import time
from gpiod.line import Direction, Value

class StepperMotor:
    """
    Klasse zur Ansteuerung eines Schrittmotors mit 4 Spulenleitungen
    (z. B. 28BYJ-48) über libgpiod. Nutzt Halbschrittmodus (8 Schritte/Zyklus).
    """

    @staticmethod
    def release():
        """
        Statische Methode: Gibt das Chip-Objekt frei, falls noch irgendwo offen.
        Falls mehrfach aufgerufen, wird ein Fehler ignoriert.
        Hinweis: Diese Methode ist optional und hängt von deinem Programmablauf ab.
        """
        try:
            chip = gpiod.Chip('/dev/gpiochip4')
            chip.close()
        except Exception:
            pass
        try:
            chip.close()
        except Exception:
            pass

    def __init__(self, in1=17, in2=18, in3=27, in4=22, chip_name='/dev/gpiochip4'):
        """
        Initialisiert den Schrittmotor.
        
        Parameter:
        -----------
        in1, in2, in3, in4 : int
            Die GPIO-Offsets für die 4 Spulenpins im Chip.
        chip_name : str
            Pfad zum GPIO-Chip (z. B. '/dev/gpiochip4').
        """

        # Pin-Offsets
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4

        # Wartezeit zwischen zwei Halbschritten. Zu klein => Gefahr von Schrittverlusten.
        self.step_sleep = 0.002

        # 4096 Halbschritte = 360° (bei 28BYJ-48 im Halbschritt-Modus)
        self.step_count = 4096

        # Richtung: True für CW (clockwise), False für CCW (counter-clockwise)
        self.direction = False  

        # Halbschritt-Sequenz (8 Schritte pro Zyklus)
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

        # LineSettings für Ausgänge
        line_settings = gpiod.LineSettings()
        line_settings.direction = Direction.OUTPUT

        # Chip öffnen und Lines anfordern
        self.chip = gpiod.Chip(chip_name)
        self.lines = self.chip.request_lines(
            consumer="StepperMotor",
            config={
                (self.in1, self.in2, self.in3, self.in4): line_settings
            }
        )

        # Pins in einer Liste -> leichteres Setzen
        self.motor_pins = [in1, in2, in3, in4]

        # Aktueller Index in der step_sequence
        self.motor_step_counter = 0

        # Merker, wie viele Schritte bisher relativ zum „Nullpunkt“ gefahren wurden
        self.steps_taken = 0

    def enable_motor(self):
        """
        Falls der Motor einen separaten ENA-Pin hätte, könnte man ihn hier aktivieren.
        Mit einem 28BYJ-48 + ULN2003 gibt es keinen separaten Enable,
        daher ist die Methode optional.
        """
        pass

    def disable_motor(self):
        """
        Deaktiviert den Motor, indem alle Ausgänge auf LOW gesetzt werden
        und gibt die reservierten Leitungen frei.
        Danach kann man keinen weiteren move() mehr machen, 
        es sei denn, man initialisiert erneut.
        """
        # Alle Pins auf LOW
        self.lines.set_values({
            self.in1: Value(0),
            self.in2: Value(0),
            self.in3: Value(0),
            self.in4: Value(0)
        })
        # Linien freigeben
        self.lines.release()
        # Chip selbst sollte offenbleiben, falls du ihn weiterverwenden willst
        # self.chip.close() -> würde den Chip komplett schließen

    def set_direction(self, direction):
        """
        Setzt die Drehrichtung. 'left' => CCW, 'right' => CW.
        """
        if direction == 'left':
            self.direction = False
        else:
            self.direction = True

    def move(self, steps):
        """
        Führt 'steps' Halbschritte aus, je nach eingestellter direction.
        steps : int
            Anzahl der Halbschritte.
        """
        for _ in range(steps):
            # Dictionary: Welcher Pin soll welchen Wert bekommen?
            # Die step_sequence gibt an, welche Spulen aktiviert werden.
            values = {
                pin: Value(val)
                for pin, val in zip(self.motor_pins, self.step_sequence[self.motor_step_counter])
            }

            # Setzt die Ausgabe auf die Pins
            self.lines.set_values(values)

            # Warte kurz, damit der Motor Zeit hat, den Schritt zu vollziehen
            time.sleep(self.step_sleep)

            # Inkrement / Dekrement des Schrittmusters
            if self.direction:
                self.motor_step_counter = (self.motor_step_counter - 1) % 8
            else:
                self.motor_step_counter = (self.motor_step_counter + 1) % 8

        # Tracke die totalen Schritte, um "move_to_original_position" zu ermöglichen
        if self.direction:
            # CW => negative Steps, falls man "Nullpunkt" links vom Start hat
            self.steps_taken -= steps
        else:
            # CCW => positive Steps
            self.steps_taken += steps

    def move_by_degree(self, degree):
        """
        Bewegt den Motor um einen Winkel 'degree' (0-360).
        4096 Halbschritte entsprechen 360 Grad => 1 Halbschritt ~ 0.088°
        """
        # Schrittberechnung für 28BYJ-48
        steps = int(self.step_count * (degree / 360.0))
        print(f"move_by_degree({degree}) => {steps} Halbschritte")
        self.move(steps)

    def move_to_original_position(self):
        """
        Fährt den Motor zurück auf Position 0,
        basierend auf der kumulierten Schrittzahl in 'self.steps_taken'.
        """
        # Merke aktuelle Richtung
        original_direction = self.direction

        # Wenn steps_taken > 0, bedeutet das, wir sind gegen den Uhrzeigersinn "rausgefahren".
        # => zurückfahren = clockwise (right) -> self.direction = True
        # (Oder umgekehrt)
        if self.steps_taken > 0:
            self.set_direction('right')
        elif self.steps_taken < 0:
            self.set_direction('left')

        # Nun absolute Schrittzahl zurückfahren
        self.move(abs(self.steps_taken))

        # Schritte sind wieder 0 (Ausgangsposition)
        self.steps_taken = 0

        # Ursprüngliche Richtung wiederherstellen
        self.direction = original_direction


if __name__ == "__main__":
    # Beispielhafter Test
    stepper = StepperMotor()
    
    # Motor "aktivieren" (falls erforderlich)
    stepper.enable_motor()
    
    # Richtung: links herum (CCW)
    stepper.set_direction('left')

    # Volle Umdrehung
    stepper.move_by_degree(360)

    # Optional: zurück zum Ursprung
    # stepper.move_to_original_position()

    # Motor deaktivieren
    stepper.disable_motor()