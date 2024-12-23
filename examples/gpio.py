import gpiod

# Wir verwenden den Context-Manager "with", um sicherzustellen,
# dass das Chip-Objekt sauber geschlossen wird, sobald wir den
# Block verlassen.
with gpiod.Chip("/dev/gpiochip4") as chip:
    # .get_info() liefert ein Objekt mit Informationen über diesen GPIO-Chip
    info = chip.get_info()

    # Dieser Aufruf chip.get_info hier wäre redundant: chip.get_info()
    # wirft keinen Fehler, aber 'chip.get_info' ohne die Klammern ruft
    # die Methode nicht erneut auf, sondern referenziert nur das Attribut.
    # Daher können wir diese Zeile entweder entfernen oder
    # bei Bedarf nochmal aufrufen:
    # info_again = chip.get_info()

    # Wir drucken die grundlegenden Informationen über den GPIO-Chip:
    # - info.name: Name des Chips (z. B. "pinctrl-bcm2835" bei einem Raspberry Pi)
    # - info.label: Zusätzliche Bezeichnung/Label des Treibers
    # - info.num_lines: Anzahl verfügbarer GPIO-Leitungen (z. B. 32 bei einem 32-pin-Chip)
    print(f"{info.name} [{info.label}] ({info.num_lines} lines)")