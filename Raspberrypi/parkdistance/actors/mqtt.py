# Vgl. https://pypi.org/project/paho-mqtt/

import paho.mqtt.client as mqtt
import dataclasses, json, logging, ssl

class MQTTHandler:
    """
    """

    def __init__(self, device, config):
        """
        Konstruktor. Im zweiten Parameter muss ein Konfigurationsobjekt mit folgenden
        Properties übergeben werden:

            * host: Hostname oder IP-Adresse des Servers
            * port: Portnummer des Servers
            * username: Benutzername (optional)
            * password: Passwort (optional)
            * keepalive: Keep-Alive Sekunden
            * tls_enable: Verschlüsselte Verbindung zulassen (optional)
            * topic_send: Topic zum Senden von Messwerten an das Backend
            * topic_recieve: Topic zum Empfangen von Befehlen aus dem Backend

        Der erste Parameter ist das `Device`-Objekt zu dem der Handler gehört. Wird
        benötigt, um in den MQTT-Threads auf das Device zugreifen zu können.
        """
        self._device = device
        self._config = config
        self._connected = False

        self._mqtt = mqtt.Client()
        self._mqtt.on_connect    = self._on_connect
        self._mqtt.on_disconnect = self._on_disconnect
        self._mqtt.on_message    = self._on_message

        logging.info(f"Stelle Verbindung zum MQTT-Server her: {config['host']}, Port {config['port']}")
        self._mqtt.connect(host=config["host"], port=int(config["port"]), keepalive=int(config["keepalive"]))

        if config.get("tls_enable", False):
            logging.info("Aktiviere TLS-Verschlüsselung für die MQTT-Kommunikation")
            self._mqtt.tls_set(tls_version=ssl.PROTOCOL_TLS)
            self._mqtt.tls_insecure_set(True)

        if config.get("username", "") or config.get("password", ""):
            logging.info(f"Führe Anmeldung am MQTT-Server durch mit Benutzername {config.get('username', '')}")
            self._mqtt.username_pw_set(username=config["username"], password=config["password"])
        
        self._mqtt.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        """
        Callback-Methode, die nach dem versuchten Verbindungsaufbau mit dem MQTT-Broker
        aufgerufen wird. Hier werden die überwachten Topics aboniert. Erfolgt hier und
        nicht im Konstruktor, damit die Abos bei einem erneuten Verbindungsaufbau nicht
        verloren gehen.

        THREADING: Diese Methode läuft im MQTT-Thread.
        """
        rc_messages = {
            0: "Verbindung hergestellt",
            1: "Fehlercode 1 - Falsche Protokollversion",
            2: "Fehlercode 2 - Ungültige Client-ID",
            3: "Fehlercode 3 - Server nicht erreichbar",
            4: "Fehlercode 4 - Benutzername/Passwort falsch",
            5: "Fehlercode 5 - Keine Berechtigung",
        }

        rc_message = rc_messages.get(rc, f"Fehlercode {rc} – Unbekannter Fehler")
        logging.info(f"Ergebnis des Verbindungsaufbaus mit dem MQTT-Broker: {rc_message}")

        if rc == 0:
            self._connected = True
            logging.info(f"Aboniere MQTT-Topic {self._config['topic_receive']}")
            self._mqtt.subscribe(self._config["topic_receive"])
        else:
            self._connected = False
    
    def _on_disconnect(self, client, userdata, rc):
        """
        Verhindert den weiteren Versand von Messwerten, solange keine Verbindung
        mit dem MQTT-Broker besteht.

        THREADING: Diese Methode läuft im MQTT-Thread.
        """
        self._connected = False
    
    def _on_message(self, client, userdata, message):
        """
        Wertet ein über MQTT empfangenes Kommando zur Fernsteuerung des Devices aus
        und führt die jeweilige Aktion direkt aus.

        THREADING: Diese Methode läuft im MQTT-Thread.
        """
        logging.info(f"Empfange Kommando für dieses Device: {message.payload}")

        payload = json.loads(message.payload)
        command = payload.get("command", "").upper()

        if command == "ALARM_ON":
            self._device.parameters["alarm"] = True
            self._device.parameters["silent"] = False
        elif command == "ALARM_OFF":
            self._device.parameters["alarm"] = False
            self._device.parameters["silent"] = False

    def __call__(self, device):
        """
        Vom Device mehrmals je Sekunde aufgerufene Funktion, um mit den Sensoren
        und Aktoren zu interagieren und die Device-Parameter zu beeinflussen.
        Sendet alle noch nicht versendeten Einträge aus `distance_measurement_ringbuffer`
        an das Backend.
        """
        for measurement in device.parameters["distance_measurement_ringbuffer"]:
            if hasattr(measurement, "_mqtt_sent"):
                continue

            self._mqtt.publish(
                qos = 0,
                topic = self._config["topic_send"],
                payload = json.dumps({
                    "command": "MEASUREMENT",
                    "data": dataclasses.asdict(measurement),
                })
            )

            measurement._mqtt_sent = True