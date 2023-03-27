import gpiozero

class DistanceSensor:
    """
    Abstandssensor zum regelmäßigen Messen der Entfernung zum nächsten Hinderniss
    """

    def __init__(self, trigger_pin, echo_pin):
        """
        Konstruktor. Parameter:
            * trigger_pin: GPIO-Pin des Trigger-Eingangs
            * echo_pin: GPIO-Pin des Echo-Ausgangs
        """
        self._sensor = gpiozero.DistanceSensor(trigger=trigger_pin, echo=echo_pin)
    
    def measure_distance(self):
        """
        Durchführen einer Abstandsmessung. Rückgabe ist der gemessene Wert in Metern.
        """
        return self._sensor.distance