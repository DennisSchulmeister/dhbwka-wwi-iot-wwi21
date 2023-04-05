import logging

class AlarmHandler:
    """"
    Handler-Klasse zum Auslösen eines globalen Alarms auf allen Devices.
    Löst einfach für jede 30ste empfangene Nachricht einen Alarm aus
    und beendet diesen wieder nach 10 weiteren Nachrichten. :-)
    """

    ALARM_ON_COUNT = 30
    ALARM_OFF_COUNT = 10
    
    def __init__(self, mqtt):
        """
        Konstruktor. Benötigt im ersten Parameter das globale MQTT-Objekt,
        um Broadcasts an die Devices senden zu können.
        """
        self._mqtt = mqtt
        self._alarm = False
        self._counter = 0
    
    def __call__(self, topic, message):
        """
        Verarbeitung einer via MQTT empfangenen Nachricht.
        """
        self._counter += 1

        if not self._alarm and self._counter == self.ALARM_ON_COUNT:
            # Alarm auslösen
            logging.info("Löse Alarm aus")

            self._counter = 0
            self._alarm   = True

            self._mqtt.broadcast({"command": "ALARM_ON"})
        elif self._alarm and self._counter == self.ALARM_OFF_COUNT:
            # Alarm beenden
            logging.info("Beende Alarm")

            self._counter = 0
            self._alarm   = False

            self._mqtt.broadcast({"command": "ALARM_OFF"})