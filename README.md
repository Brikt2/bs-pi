[Unit]
Description=Entur Controller Button Service
After=network.target

[Service]
# Bruk 'pi' som eier av prosessen
User=pi
WorkingDirectory=/home/pi/entur_project

# Start-kommando (juster stien om nødvendig)
ExecStart=/usr/bin/python3 /home/pi/entur_project/controller_button.py

# Restart hvis scriptet krasjer
Restart=always
RestartSec=5

# Sørg for at GPIO får tilgang
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
