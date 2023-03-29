import gpiozero, logging

from collections import deque
from dataclasses import dataclass
from datetime import datetime

class DistanceSensor:
    """
    Abstandssensor zum regelmäßigen Messen der Entfernung zum nächsten Hinderniss.
    """

    def __init__(self, trigger_pin, echo_pin, ringbuffer_size):
        """
        Konstruktor. Parameter:
            * trigger_pin: GPIO-Pin des Trigger-Eingangs
            * echo_pin: GPIO-Pin des Echo-Ausgangs
        """
        self._sensor = gpiozero.DistanceSensor(trigger=trigger_pin, echo=echo_pin)
        self._ringbuffer_size = ringbuffer_size
    
    def measure_distance(self):
        """
        Durchführen einer Abstandsmessung. Rückgabe ist der gemessene Wert in Metern.
        """
        return round(self._sensor.distance, 2)

    def __call__(self, device):
        """
        Vom Device mehrmals je Sekunde aufgerufene Funktion, um mit den Sensoren
        und Aktoren zu interagieren und die Device-Parameter zu beeinflussen.
        Steuert folgende Device-Paramater:

            * distance_measurement_ringbuffer: Letzte N Abstandsmessungen mit Zeitstempel
            * current_distance_m: Aktuell gemessener Abstand in Metern
        """
        # Letzte N Messungen zwischenspeichern
        measurement = DistanceMeasurement(
            distance_m   = self.measure_distance(),
            datetime_iso = datetime.now().isoformat()
        )

        if not "distance_measurement_ringbuffer" in device.parameters:
            device.parameters["distance_measurement_ringbuffer"] = deque(maxlen=self._ringbuffer_size)
        
        device.parameters["distance_measurement_ringbuffer"].append(measurement)

        # Aktuellen Messwert für leichteren Zugriff separat ablegen
        device.parameters["current_distance_m"] = measurement.distance_m
        logging.info(f"Gemessener Abstand: {measurement.distance_m} m")

@dataclass
class DistanceMeasurement:
    """
    Wert einer einzelnen Abstandsmessung mit Zeitstempel.
    """
    distance_m: float
    datetime_iso: str
