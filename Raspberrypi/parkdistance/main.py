import configparser, gpiozero, logging, os, time
from parkdistance.device import Device
from parkdistance.sensors.button import SilentButton
from parkdistance.sensors.distance import DistanceSensor
from parkdistance.actors.led_beeper import LedBeeper
from parkdistance.actors.mqtt import MQTTHandler

def main():
    """
    Zentraler Einstiegspunkt in das Programm. Erzeugt alle benötigten Objekte
    und sorgt dafür, dass das Programm im Hintergrund laufen kann.
    """
    # Logging konfigurieren
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logging.info("parkdistance sagt Hallo!")

    # pigpio-Bibliothek für höhere Genauigkeit verwenden, falls installiert
    try:
        from gpiozero.pins.pigpio import PiGPIOFactory
        from gpiozero import Device as GPIOZeroDevice
        GPIOZeroDevice.pin_factory = PiGPIOFactory()
        logging.info("Benutze pigpio für höhere Genauigkeit")
    except:
        pass

    # Konfigurationsdatei einlesen
    configfile = os.path.join(os.path.dirname(__file__), "..", "config.ini")
    config = configparser.ConfigParser(interpolation=None)
    config.read(configfile)

    # Device, Sensoren und Aktoren konfigurieren
    try:
        device = Device()

        device.add_sensor_actor(SilentButton(pin=23, pull_up=True))
        device.add_sensor_actor(DistanceSensor(trigger_pin=10, echo_pin=9, ringbuffer_size=10))
        device.add_sensor_actor(LedBeeper(led1_pin=7, led2_pin=8, buzzer_pin=13))
        device.add_sensor_actor(MQTTHandler(device, config["mqtt"]))

        device.loop_forever(update_frequency=1)
    except KeyboardInterrupt:
        pass

    ## Alte Version ohne Entkopplung der Objekte durch die Device-Klasse.
    ## Für kleinere Anwendungen ist diese Version auch gut bzw. sogar
    ## etwas einfacher zu verstehen. Je mehr Sensoren und Aktoren jedoch
    ## hinzu kommen, desto unübersichtlicher wird der Quellcode zu ihrer
    ## Verknüpfung und desto weniger lässt sich das Offen/Geschlossen-Prinzip
    ## beim Hinzufügen weiterer Sensoren oder Aktoren einhalten.
    #
    # distance_min_m = 0.1
    # distance_max_m = 1.0
    #
    # try:
    #     while True:
    #         time.sleep(0.5)
    #
    #         distance_m = distance_sensor.measure_distance()
    #         print(f"Gemessener Abstand: {distance_m}")
    #
    #         if silent_button.value == silent_button.PRESSED:
    #             led_beeper.silent = not led_beeper.silent
    #             print(f"Ton aus? {led_beeper.silent}")
    #
    #         intensity = 1.0 * (distance_m - distance_min_m) / (distance_max_m - distance_min_m)
    #         intensity = 1 - intensity
    #         led_beeper.intensity = intensity
    # except KeyboardInterrupt:
    #     pass