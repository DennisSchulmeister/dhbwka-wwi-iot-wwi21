import gpiozero

class StartStopButton:
    """
    Diese Klasse überwacht einen Hardwarebutton, mit dem die Messung
    ein- oder ausgeschaltet werden kann. Zusätzlich kann durch langes
    Gedrückthalten des Buttons ein vom Backend gemeldeter Alarm
    deaktiviert werden.
    """

    NOT_PRESSED = 0
    PRESSED = 1
    HELD = 2

    def __init__(self, pin, pull_up=False, bouncetime=0.2):
        """
        Konstruktor. Parameter:
            * pin: GPIO-Pin des Buttons
            * pull_up: Aktivierung des internen Pull-Up-Widerstands
            * bouncetime: Entprellzeit des Buttons in Sekunden
        """
        self._button = gpiozero.Button(pin=pin, pull_up=pull_up, bouncetime=bouncetime)
    
    @property
    def value(self):
        """
        Property mit dem aktuellen Wert des Buttons.
        0 = Nicht gedrückt, 1 = Kurz gedrückt, 2 = Gedrückt gehalten.
        Für die Werte gibt es in der Klasse entsprechende Konstanten.
        """
        if self._button.is_held:
            return self.HELD
        elif self._button.is_pressed:
            return self.PRESSED
        else:
            return self.NOT_PRESSED