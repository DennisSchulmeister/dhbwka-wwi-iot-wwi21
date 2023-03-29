import logging, time

class Device:
    """
    Klasse zur Steuerung des Devoces. Beinhaltet die Hauptschleife des Programms,
    in der mehrmals je Sekunde die Sensoren abgefragt und die Deviceparameter
    entsprechend aktualisiert werden. Anhand dieser werden dann die dazugehörigen
    Aktoren angesteurt.

    Die Device-Parameter finden sich im Dictionary `self.parameters`, das von den
    Sensoren und Aktoren entsprechend verwendet wird.
    """
    
    def __init__(self):
        """
        Konstruktor.
        """
        self._sensors = []
        self._actors  = []

        self.parameters = {}
    
    def add_sensor(self, sensor):
        """
        Sensor dem Device hinzufügen. Bei dem übergebenen Sensorbjekt muss es sich
        um ein Callable handeln (Funktion oder Objekt mit `__call__()`-Methode),
        dass als einzigen Parameter das Device-Objekt übergeben bekommt.

        Aufgabe der Sensoren ist es, die Deviceparameter zu ändern, anhand derer
        die Entscheidungen zum Verhalten des Devices getroffen werden. Die Sensoren
        werden daher immer am *Anfang* der Hauptschleife vor Berechnung der Aktionen
        angesteuert.
        """
        self._sensors.append(sensor)
    
    def add_actor(self, actor):
        """
        Aktor dem Device hinzufügen. Bei dem übergebenen Aktorobjekt muss es sich
        um ein Callable handeln (Funktion oder Objekt mit `__call__()`-Methode),
        dass als einzigen Parameter das Device-Objekt übergeben bekommt.

        Aufgabe der Aktoren ist es, das auf Basis der Sensorwerte ermittelte Verhalten
        des Devices auszuführen. Die Aktoren werden daher immer am *Ende* der Hauptschleife
        nach Berechnung der Aktionen angesteuert.
        """
        self._actors.append(actor)

    def loop_forever(self, update_frequency=10):
        """
        Hauptschleife zur Steuerung des Devices. Muss aufgerufen werden, damit das
        Device regelmäßig seine Sensoren prüft und basierend auf den erhaltenen Werten
        die Parameter ändert und die Aktoren ansteuert.

        Parameter:
            * update_frequency: Anzahl der Sensorprüfungen pro Sekunde.
        """
        target_delay_s = 1.0 / update_frequency
        prev_time_s = 0
        needed_delay_s = 0

        while True:
            # Thread pausieren, um CPU-Leistung einzusparen
            current_time_s = time.monotonic()
            needed_delay_s = target_delay_s - (current_time_s - prev_time_s)
            prev_time_s = current_time_s

            if needed_delay_s > 0:
                time.sleep(needed_delay_s)
            
            # Sensoren auslesen
            for sensor in self._sensors:
                sensor(self)
            
            # Aktoren auslesen
            for actor in self._actors:
                actor(self)