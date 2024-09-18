import gpiod
import time

def manual_gpio_test():
    chip = gpiod.Chip('gpiochip0')
    
    DIR = chip.get_line(17)  # Direction Pin
    PUL = chip.get_line(27)  # Pulse Pin
    ENA = chip.get_line(22)  # Enable Pin

    DIR.request(consumer='manual-test', type=gpiod.LINE_REQ_DIR_OUT)
    PUL.request(consumer='manual-test', type=gpiod.LINE_REQ_DIR_OUT)
    ENA.request(consumer='manual-test', type=gpiod.LINE_REQ_DIR_OUT)

    try:
        # Aktivierung des Motors
        ENA.set_value(0)  # Set ENA to LOW to enable the motor
        print("ENA (Enable) auf LOW gesetzt, Motor sollte aktiviert sein.")
        DIR.set_value(1)
        for i in range(200):
            i = i + 1
            PUL.set_value(0)
            time.sleep(0.001)
            PUL.set_value(1)
            time.sleep(0.001)
        
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

    finally:
        ENA.set_value(1)  # Set ENA to HIGH to disable the motor
        chip.close()
        print("Motor deaktiviert und GPIO-Ressourcen freigegeben.")

manual_gpio_test()