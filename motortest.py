import gpiod
import time

def manual_gpio_test():
    """
    Diese Funktion demonstriert, wie man mit gpiod einzelne GPIO-Leitungen abfragt 
    und setzt, um einen Motor-Treiber manuell zu testen.

    Annahmen/Überlegungen:
    - Wir greifen auf gpiochip0 zu. Je nach Board (z. B. Raspberry Pi) kann das 
      auch gpiochip1 oder ein anderer Chip sein. 
    - Die Leitungs-Offsets (17, 27, 22) müssen entsprechend der tatsächlichen 
      Verkabelung angepasst werden. 
    - ENA/Enable-Pin: Aktiviert/Deaktiviert den Motor (LOW = aktiv, HIGH = inaktiv).
    - DIR/Direction-Pin: Bestimmt die Drehrichtung (0 oder 1). 
    - PUL/Pulse-Pin: Jeder LOW->HIGH-Puls entspricht einem Mikroschritt bzw. 
      Schritt, abhängig vom Motor-/Treiber-Setup.
    """

    # Öffnet das Device /dev/gpiochip0 
    chip = gpiod.Chip('gpiochip0')
    
    # Wir holen uns drei Leitungen nach ihrem Offset:
    #  - DIR (Direction Pin)
    #  - PUL (Pulse Pin)
    #  - ENA (Enable Pin)
    DIR = chip.get_line(17)
    PUL = chip.get_line(27)
    ENA = chip.get_line(22)

    # Wir fordern die Lines mit der gewünschten Richtung an:
    #   type=gpiod.LINE_REQ_DIR_OUT  -> Ausgang
    #   consumer='manual-test'       -> beliebiger Name der Anwendung
    DIR.request(consumer='manual-test', type=gpiod.LINE_REQ_DIR_OUT)
    PUL.request(consumer='manual-test', type=gpiod.LINE_REQ_DIR_OUT)
    ENA.request(consumer='manual-test', type=gpiod.LINE_REQ_DIR_OUT)

    try:
        # ENA auf LOW setzen, um den Motor zu aktivieren
        ENA.set_value(0)
        print("ENA (Enable) auf LOW gesetzt, Motor sollte aktiviert sein.")
        
        # DIR auf 1 setzen => z. B. 'Vorwärts'-Drehrichtung, je nach Treiber
        DIR.set_value(1)

        # 200 Pulse senden => könnte bei manchen Treibern 200 Mikroschritte bedeuten
        # oder 200 Vollschritte (abhängig vom Treiber).
        # Die Wartezeit (0.001 Sek.) bestimmt die Geschwindigkeit.
        for i in range(200):
            # Schritt: PUL auf 0
            PUL.set_value(0)
            time.sleep(0.001)
            
            # Schritt: PUL auf 1
            PUL.set_value(1)
            time.sleep(0.001)
        
        print("200 Pulse gesendet. Motor sollte sich bewegt haben.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

    finally:
        # ENA auf HIGH => Motor deaktivieren
        ENA.set_value(1)
        
        # Chip schließen, damit die Lines freigegeben werden
        chip.close()
        print("Motor deaktiviert und GPIO-Ressourcen freigegeben.")


if __name__ == "__main__":
    manual_gpio_test()