import gpiozero, time

def main():
    """
    Zentraler Einstiegspunkt in das Programm. Erzeugt alle benötigten Objekte
    und sorgt dafür, dass das Programm im Hintergrund laufen kann.
    """
    print("parkdistance sagt Hallo!")

    # Hardwarebausteine ansprechen
    button = gpiozero.Button(pin=23, bounce_time=0.2)
    buzzer = gpiozero.Buzzer(13)
    led1 = gpiozero.LED(7)
    led2 = gpiozero.LED(8)
    distance_sensor = gpiozero.DistanceSensor(trigger=10, echo=9, max_distance=1)

    led1.off()
    led2.off()

    try:
        while True:
            time.sleep(0.1)
            buzzer.value = button.value
            led1.value = button.value

            if button.value:
                led2.off()
            else:
                led2.on()

            if button.value:
                print("Button wurde gedrückt")
            
            print(distance_sensor.distance)
    except KeyboardInterrupt:
        pass