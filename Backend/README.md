IoT-Backend
===========

Dies ist der Quellcode, der lokal auf dem eigenen Laptop entwickelt und später
in irgend einem Rechenzentrum ausgeführt werden muss. Besteht aus folgenden
Komponenten:

 * Simple Logger: Python-Anwendung zum Speichern der Messwerte
 * MongoDB: Datenbank
 * Mongo-Express: Weboberfläche für die Mongo-Datenbank
 * EMQX: Lokaler MQTT-Broker (optional)

Mit Docker Compose können die Services wie folgt gestartet werden:

    ```sh
    docker compose --profile dev --profile mqtt --profile prod up
    ```

Die beiden Profilparameter sind optional, steuern aber folgendes:

    * `--profile dev`: Für die Entwicklung nützliche Dienste starten, wie Mongo-Express
    * `--profile mqtt`: Lokalen MQTT-Server starten
    * `--profile prod`: Python-Anwendung als Docker Container verpacken und starten

Für die Entwicklung sollte Python besser lokal ausgeführt werden, um Änderungen
am Code schneller testen zu können. Bei Verwendung eines öffentlichen MQTT-Brokers
wie dem [HiveMQ Public Broker](https://www.hivemq.com/public-mqtt-broker/) würde
man also folgenden Befehl zum Starten verwenden:

    ```sh
    docker compose --profile dev up
    ```