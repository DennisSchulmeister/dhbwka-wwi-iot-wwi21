import gpiozero, logging

class SilentButton:
    """
    Diese Klasse überwacht einen Hardwarebutton, mit dem die Töne beim Messe
    ein- oder ausgeschaltet werden können. Zusätzlich kann durch langes Drücken
    des Buttons ein vom Backend gemeldeter Alarm stummgeschaltet werden.
    """

    NOT_PRESSED = 0
    PRESSED = 1
    HELD = 2

    def __init__(self, pin, pull_up=False, bounce_time=0.3):
        """
        Konstruktor. Parameter:
            * pin: GPIO-Pin des Buttons
            * pull_up: Aktivierung des internen Pull-Up-Widerstands
            * bouncetime: Entprellzeit des Buttons in Sekunden
        """
        self._button = gpiozero.Button(pin=pin, pull_up=pull_up, bounce_time=bounce_time, hold_time=1.0)            
        self._locked = False

    @property
    def value(self):
        """
        Property mit dem aktuellen Wert des Buttons.
        0 = Nicht gedrückt, 1 = Kurz gedrückt
        Für die Werte gibt es in der Klasse entsprechende Konstanten.
        """
        if self._button.is_pressed:
            return self.PRESSED
        else:
            return self.NOT_PRESSED
    
    def __call__(self, device):
        """
        Vom Device mehrmals je Sekunde aufgerufene Funktion, um mit den Sensoren
        und Aktoren zu interagieren und die Device-Parameter zu beeinflussen.
        Steuert folgende Device-Paramater:

            *silent: Tonausgabe unterdrücken (Boolean)
        """
        if not "silent" in device.parameters:
            device.parameters["silent"] = False

        if self.value == self.PRESSED:
            if not self._locked:
                self._locked = True
                device.parameters["silent"] = not device.parameters["silent"]
                logging.info(f"Silent-Button gedrückt! Setze silent={device.parameters['silent']}")
        else:
            self._locked = False
        