import logging, os
from pymongo import MongoClient

class MongoDBHandler:
    """
    Handler-Klasse zum Speichern empfangener Messwerte in einer Mongo-Datenbank.
    Ein Objekt dieser Klasse wird vom zentralen MQTT-Objekt für jede empfangene
    Nachricht aufgerufen. Hier wird dann geprüft, ob es sich um einen Messwert
    handelt und dieser dann abgespeichert.
    """
    
    def __init__(self, config):
        """
        Konstruktor. Im zweiten Parameter muss ein Konfigurationsobjekt mit folgenden
        Properties übergeben werden:

            * connection: URL für die Verbindung zur Datenbank, zum Beispiel:
              "mongodb://dbuser:dbpass@mongodb:27017/"
        """
        connection = os.getenv("MONGO_DB_CONNECTION") or config['connection']
        logging.info(f"Stelle Verbindung zur Datenbank her: {connection}")

        self._mongo = MongoClient(connection)
        self._database = self._mongo.get_database("sensor_db")
        self._measurements = self._database.get_collection("measurements")

        logging.info(f"self._mongo = {self._mongo}")
        logging.info(f"self._database = {self._database}")
        logging.info(f"self._measurements = {self._measurements}")
    
    def __call__(self, topic, message):
        """
        Verarbeitung einer via MQTT empfangenen Nachricht.
        """
        try:
            command = message.get("command", "")
        except AttributeError:
            return
        
        if not command == "MEASUREMENT":
            return
        
        document = {
            "device": topic,
            "data": message.get("data", {})
        }

        logging.info(f"Speichere Messwert: {document}")

        self._measurements.insert_one(document)

        logging.info(f"Gespeicherter Messwert: {document['_id']}")