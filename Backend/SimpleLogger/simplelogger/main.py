import configparser, logging, os, time

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

    logging.info("simplelogger sagt Hallo!")

    # Konfigurationsdatei einlesen
    configfile = os.path.join(os.path.dirname(__file__), "..", "config.ini")
    config = configparser.ConfigParser(interpolation=None)
    config.read(configfile)