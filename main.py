from gpiozero import LED
import time

led = LED(18)

print("Scriptet kjører... LED på!")
led.on()

