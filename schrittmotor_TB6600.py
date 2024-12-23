import gpiod
import time

class StepperMotor:
    """
    Klasse zum Ansteuern eines Schrittmotors über drei GPIO-Ausgänge (DIR, PUL, ENA)
    und einen GPIO-Eingang (SWITCH = Mikroschalter).
    
    Nutzung von gpiod:
      - 'chip_name': Name des GPIO-Chips, z. B. 'gpiochip0'
      - get_line(X): holt die Leitung mit Offset X (nicht unbedingt identisch mit BCM-Nummern)
      - request(...): legt fest, ob diese Line Eingang oder Ausgang ist.
    """

    def __init__(self, chip_name='gpiochip0', DIR=17, PUL=27, ENA=22, SWITCH=12):
        """
        Initialisiert den Chip, richtet die Pinmodi (Eingang/Ausgang) ein 
        und deaktiviert den Motor standardmäßig.
        
        Parameter:
        -----------
        chip_name : str
            Name des GPIO-Chips, meist 'gpiochip0' auf einem System mit einem SoC.
        DIR : int
            GPIO-Offset für den DIR-Pin (Direction).
        PUL : int
            GPIO-Offset für den PUL-Pin (Pulse).
        ENA : int
            GPIO-Offset für den ENA-Pin (Enable).
        SWITCH : int
            GPIO-Offset für den Mikroschalter, der z. B. den Nullpunkt erkennt.
        """
        print("Initialisiere GPIO...")
        self.chip = gpiod.Chip(chip_name)

        # Hole die GPIO-Lines
        self.DIR = self.chip.get_line(DIR)
        self.PUL = self.chip.get_line(PUL)
        self.ENA = self.chip.get_line(ENA)
        self.SWITCH = self.chip.get_line(SWITCH)

        # Für die Richtungs- und Enable-Logik definieren wir Konstanten
        self.DIR_Left = 0
        self.DIR_Right = 1

        self.ENA_Locked = 0     # Motor aktiv
        self.ENA_Released = 1   # Motor deaktiviert

        # GPIO-Linien für DIR, PUL, ENA als Ausgang
        self.DIR.request(consumer='stepper-motor', type=gpiod.LINE_REQ_DIR_OUT)
        self.PUL.request(consumer='stepper-motor', type=gpiod.LINE_REQ_DIR_OUT)
        self.ENA.request(consumer='stepper-motor', type=gpiod.LINE_REQ_DIR_OUT)

        # Mikroschalter als Eingang mit Pull-Up-Widerstand
        # So liegt SWITCH im Ruhezustand auf HIGH (1).
        # Wird der Schalter gedrückt, zieht er die Leitung auf LOW (0).
        self.SWITCH.request(
            consumer='stepper-motor', 
            type=gpiod.LINE_REQ_DIR_IN,
            flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP
        )

        # Motor standardmäßig deaktivieren
        self.disable_motor()

    def enable_motor(self):
        """
        Schaltet den Motor ein, indem ENA auf das 'Locked'-Signal gesetzt wird (typischerweise LOW).
        """
        print("Motor wird aktiviert (Enable auf LOW)...")
        self.ENA.set_value(self.ENA_Locked)

    def disable_motor(self):
        """
        Schaltet den Motor aus, indem ENA auf das 'Released'-Signal gesetzt wird (typischerweise HIGH).
        """
        print("Motor wird deaktiviert (Enable auf HIGH)...")
        self.ENA.set_value(self.ENA_Released)

    def set_direction(self, direction):
        """
        Setzt die Drehrichtung: 'left' oder 'right'.
        
        Parameter:
        -----------
        direction : str
            'left' oder 'right'
        """
        direction_lower = direction.lower()
        if direction_lower == 'left':
            print("Setze Richtung auf: Links (DIR=0)")
            self.DIR.set_value(self.DIR_Left)
        elif direction_lower == 'right':
            print("Setze Richtung auf: Rechts (DIR=1)")
            self.DIR.set_value(self.DIR_Right)
        else:
            raise ValueError("Richtung muss entweder 'left' oder 'right' sein.")

    def move(self, steps, delay=0.001):
        """
        Bewegt den Motor eine bestimmte Anzahl von Schritten.
        Unterbricht die Bewegung, falls der Mikroschalter ausgelöst wird.

        Parameter:
        -----------
        steps : int
            Anzahl der Schritte, die der Motor ausführen soll.
        delay : float
            Verzögerung zwischen den Pulsen in Sekunden (steuert die Geschwindigkeit).
        """
        print(f"Bewege Motor für {steps} Schritte mit delay={delay:.4f}s.")
        for _ in range(steps):
            # Prüfen, ob Schalter gedrückt ist (Wert = 0 => LOW)
            if self.SWITCH.get_value() == 0:
                print("Schalter betätigt! Motor wird gestoppt.")
                break
            
            # Pulse erzeugen: 1 -> 0 oder 0 -> 1
            self.PUL.set_value(1)
            time.sleep(delay)
            self.PUL.set_value(0)
            time.sleep(delay)

    def move_to_zero_point(self, delay=0.001):
        """
        Bewegt den Motor (in Richtung 'left') solange, bis der Mikroschalter gedrückt ist (SWITCH=0).
        Beispiel: Endschalter-Mechanismus für Home-Position.
        """
        print("Bewege Motor zum Nullpunkt (Nach links, bis SWITCH=0)...")
        self.set_direction('left')
        
        # Solange der Schalter nicht betätigt ist (SWITCH=1 = HIGH), Motor weiterbewegen
        while self.SWITCH.get_value() == 1:
            self.PUL.set_value(1)
            time.sleep(delay)
            self.PUL.set_value(0)
            time.sleep(delay)
        
        print("Nullpunkt erreicht (SWITCH=0).")

    def move_by_degree(self, degree, delay=0.001, microsteps=8):
        """
        Bewegt den Motor um 'degree' Grad, unter Berücksichtigung von Mikroschritten.
        Eine Umdrehung = 360°, ein typischer Schrittmotor hat 200 Schritte/Umdrehung im Vollschritt.
        
        Parameter:
        -----------
        degree : float
            Winkel in Grad, um den der Motor bewegt werden soll.
        delay : float
            Wartezeit zwischen Pulsen (steuert Geschwindigkeit).
        microsteps : int
            Gibt das Mikroschrittverhältnis an (z. B. 8 bedeutet 1600 Schritte pro Umdrehung).
        
        Beispiel:
            move_by_degree(90, microsteps=8) => 1/4 Umdrehung im 1/8-Schritt-Modus = 200 * 8 * 90/360
        """
        steps_per_revolution = 200 * microsteps
        steps = int((degree / 360.0) * steps_per_revolution)
        print(f"Bewege um {degree}° => {steps} Schritte (Mikrostepping={microsteps}, delay={delay:.4f}s)")
        self.move(steps, delay)

    def cleanup(self):
        """
        Schließt den Chip (gibt die Leitungen frei). 
        Sollte am Ende der Anwendung aufgerufen werden.
        """
        print("GPIO-Ressourcen werden freigegeben...")
        self.chip.close()


if __name__ == "__main__":
    # Beispielhafte Nutzung:
    # 1. Motor-Objekt anlegen
    stepper = StepperMotor()

    # 2. Motor aktivieren
    stepper.enable_motor()

    # 3. Richtung auf 'left' stellen und 90° drehen
    stepper.set_direction('left')
    stepper.move_by_degree(90, delay=0.001)

    # 4. Motor deaktivieren und ggf. eine Pause
    stepper.disable_motor()
    time.sleep(2)

    # 5. Erneut aktivieren und zum Nullpunkt fahren
    stepper.enable_motor()
    stepper.move_to_zero_point(delay=0.001)

    # 6. Aufräumen
    stepper.cleanup()