from gpiozero import Button
import os
import subprocess
import time

# GPIO 17
button = Button(17)

def update_and_run():
    print("Oppdaterer fra GitHub...")
    os.chdir("/home/pi/dittrepo")
    subprocess.run(["git", "pull"])
    print("Starter script...")
    subprocess.run(["python3", "main.py"])

print("Klar. Trykk på knappen for å oppdatere og kjøre scriptet.")
while True:
    button.wait_for_press()
    update_and_run()
    time.sleep(1)
