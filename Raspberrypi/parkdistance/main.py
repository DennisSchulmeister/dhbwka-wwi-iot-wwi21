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

        device.add_sensor(SilentButton(pin=23, pull_up=True))
        device.add_sensor(DistanceSensor(trigger_pin=10, echo_pin=9, ringbuffer_size=10))

        device.add_actor(LedBeeper(led1_pin=7, led2_pin=8, buzzer_pin=13))
        device.add_actor(MQTTHandler(device, config["mqtt"]))

        device.loop_forever(update_frequency=1)
    except KeyboardInterrupt:
        pass