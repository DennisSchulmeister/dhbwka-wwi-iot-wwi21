import gpiozero, threading, time, logging

class LedBeeper:
    """
    Status-LED und Buzzer, die in Abhängigkeit von der gemessenen Entfernung
    unterschiedlich schnell einen periodischen Signalton ausgeben und blinken.
    """

    def __init__(self, led1_pin, led2_pin, buzzer_pin, distance_min_m=0.1, distance_max_m=1.0):
        """
        Konstruktor. Parameter:
            * led1_pin: GPIO-Pin der roten LED
            * led2_pin: GPIO-Pin der gründen LED
            * buzzer_pin: GPIO-Pin des Buzzers
        """
        self._led1   = gpiozero.DigitalOutputDevice(pin=led1_pin)
        self._led2   = gpiozero.DigitalOutputDevice(pin=led2_pin)
        self._buzzer = gpiozero.DigitalOutputDevice(pin=buzzer_pin)

        self._intensity = 0
        self._distance_min_m = distance_min_m
        self._distance_max_m = distance_max_m

        self.alarm  = False
        self.silent = False

        self._blink_thread = threading.Thread(target=self._blink_thread_main)
        self._blink_thread.start()

    @property
    def intensity(self):
        """
        Property zum Auslesen der aktuellen Alarmintensität als Float.
        0 = Alarm aus ... 1 = Dauerton; dazwischen wiederholtes Piepsen.
        """
        return self._intensity

    @intensity.setter
    def intensity(self, intensity):
        """
        Alarm ertönen lassen bzw. wieder ausschalten durch Überschreiben
        der Alarmintensität. Die Alarmintensität schwankt je nach Wert
        von 2 bis 10 Tönen je Sekunde bzw. danach einem Dauerton.
        """
        if intensity < 0:
            intensity = 0
        elif intensity > 1:
            intensity = 1

        self._intensity = intensity

    def _blink_thread_main(self):
        """
        Hintergrundthread zum periodischen Ein- und Ausschalten der Ausgänge.
        Ist leider etwas umständlich, aber mit Pulsweitemodulierten Pins können
        nur Frequenzen wie 10 Hz, 20 Hz oder 40 Hz geschaltet werden. Wir wollen
        aber variabel von 1x/Sekunde bis 10x/Sekunde blinken können.
        """
        while True:
            if self.intensity < 0.1:
                # Alles aus
                self._led1.off()
                self._led2.off()
                self._buzzer.off()
            elif self.intensity > 0.9:
                # Crash oder Alarm: Alles an
                if self.alarm:
                    self._led1.on()
                    self._led2.off()
                else:
                    self._led1.off()
                    self._led2.on()

                if not self.silent:
                    self._buzzer.on()
                else:
                    self._buzzer.off()
            else:
                # Normale Messung: Periodisches Blinken/Piepsen
                frequency = 15 * self.intensity
                sleep_time_s = 1.0 / frequency

                self._led1.off()
                self._led2.on()

                if not self.silent:
                    self._buzzer.on()
                else:
                    self._buzzer.off()

                time.sleep(sleep_time_s)

                self._led1.off()
                self._led2.off()
                self._buzzer.off()

                time.sleep(sleep_time_s)

    def __call__(self, device):
        """
        Vom Device mehrmals je Sekunde aufgerufene Funktion, um mit den Sensoren
        und Aktoren zu interagieren und die Device-Parameter zu beeinflussen.
        Reagiert auf folgende Device-Parameter:

            * current_distance_m: Aktuell gemessener Abstand in Metern
            * silent: Tonausgabe unterdrücken (Boolean)
            * alarm: Vom Backend ausgelöster Alarm (Boolean)
        """
        self.silent = device.parameters.get("silent", False)
        self.alarm = device.parameters.get("alarm", False)

        if self.alarm:
            self.intensity = 1
        else:
            distance_m = device.parameters.get("current_distance_m", 9999)

            if self._distance_min_m <= distance_m <= self._distance_max_m:
                self.intensity = 1.0 * (distance_m - self._distance_min_m) / (self._distance_max_m - self._distance_min_m)
                self.intensity = 1 - self.intensity
            else:
                self.intensity = 0.0
