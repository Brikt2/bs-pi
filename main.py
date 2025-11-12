from gpiozero import LED
import time

led = LED(18)

print("Scriptet kjører... LED ble ikke på alikevel!")
led.on()

