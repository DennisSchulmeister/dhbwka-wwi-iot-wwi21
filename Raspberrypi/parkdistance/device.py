import time, traceback

class Device:
    """
    Klasse zur Steuerung des Devices und seines Gesamtzustands. Beinhaltet die
    Hauptschleife des Programms, in der mehrmals je Sekunde die Sensoren abgefragt
    und die Deviceparameter entsprechend aktualisiert werden. Anhand dieser werden
    dann die Aktoren angesteuert.

    Die Device-Parameter befinden sich im Dictionary `self.parameters`, das von
    den Sensoren und Aktoren verwendet wird.
    """

    def __init__(self):
        """
        Konstruktor.
        """
        self._sensors_actors = []
        self.parameters = {}

    def add_sensor_actor(self, sensor_actor):
        """
        Sensor oder Aktor dem Device hinzufügen, damit er in der Hauptschleife
        des Devices periodisch abgefragt werden kann. Das übergebene Objekt
        muss ein Callable sein, das als einzigen Parameter ein `Device`-Objekt
        erwartet.
        """
        self._sensors_actors.append(sensor_actor)
    
    def loop_forever(self, update_frequency=2):
        """
        Hauptschleife zur Steuerung des Devices. Muss im Hauptprogramm aufgerufen
        werden, damit das Device periodisch seine Sensoren und Aktorek aufrufen
        kann und diese ihre Logik ausführen.
        """
        max_sleep_time_s = 1.0 / update_frequency
        actual_sleep_time_s = 0.0
        prev_time_s = 0.0

        while True:
            # Variable Dauer abwarten, um die gewünschte Update-Frequenz zu erhalten
            current_time_s = time.monotonic()
            actual_sleep_time_s = max_sleep_time_s - (current_time_s - prev_time_s)
            prev_time_s = current_time_s

            if actual_sleep_time_s > 0:
                time.sleep(actual_sleep_time_s)

            # Logik der Sensoren und Aktoren ausführen
            for sensor_actor in self._sensors_actors:
                try:
                    sensor_actor(self)
                except KeyboardInterrupt:
                    return
                except:
                    traceback.print_exc()