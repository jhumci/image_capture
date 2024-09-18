import gpiod

# Versuche, den GPIO-Chip zu öffnen
try:
    chip = gpiod.Chip('gpiochip0')
    print("GPIO-Chip 'gpiochip0' erfolgreich geöffnet.")
except FileNotFoundError:
    print("GPIO-Chip 'gpiochip0' konnte nicht gefunden werden.")
    exit(1)
except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")
    exit(1)

# Versuche, die GPIO-Linien zu bekommen
try:
    lines = chip.get_lines([4, 17, 27, 22])
    print("GPIO-Linien erfolgreich zugewiesen.")
except Exception as e:
    print(f"Ein Fehler ist beim Zuweisen der GPIO-Linien aufgetreten: {e}")
    exit(1)

# Versuche, die GPIO-Linien als Ausgang zu konfigurieren und Werte zu setzen
try:
    lines.request(consumer='test', type=gpiod.LINE_REQ_DIR_OUT)
    print("GPIO-Linien erfolgreich als Ausgang konfiguriert.")
    
    lines.set_values([0, 1, 0, 1])
    print("Werte wurden erfolgreich auf die GPIO-Linien geschrieben.")
except Exception as e:
    print(f"Ein Fehler ist beim Setzen der GPIO-Werte aufgetreten: {e}")
