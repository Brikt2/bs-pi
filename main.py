# entur_bus_timer.py
import requests
import datetime
import threading
import os

ENTUR_URL = "https://api.entur.io/journey-planner/v3/graphql"
STOP_PLACE_ID = "NSR:StopPlace:6435"
INTERVAL = 30  # sekunder

SENTRUM = ["Kværnerbyen", "Ekeberg hageby"]
OTHER_WAY = ["Kjelsås stasjon", "Tåsen"]

QUERY = f"""
{{
  stopPlace(id: "{STOP_PLACE_ID}") {{
    id
    name
    estimatedCalls(timeRange: 72100, numberOfDepartures: 12) {{
      realtime
      aimedArrivalTime
      expectedArrivalTime
      destinationDisplay {{ frontText }}
      serviceJourney {{
        journeyPattern {{
          line {{ id transportMode }}
        }}
      }}
    }}
  }}
}}
"""

# global variabel for å holde Timer-objektet
update_timer = None
running = False


def fetch_departures():
    try:
        response = requests.post(
            ENTUR_URL,
            headers={
                "Content-Type": "application/json",
                "ET-Client-Name": "Infoboard-app",
            },
            json={"query": QUERY},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data["data"]["stopPlace"]["estimatedCalls"]
    except Exception as e:
        print("Feil ved henting:", e)
        return []


def print_departures(deps, tittel):
    now = datetime.datetime.now(datetime.timezone.utc)
    print(f"\n{tittel}:")
    for dep in deps:
        front = dep["destinationDisplay"]["frontText"]
        line = dep["serviceJourney"]["journeyPattern"]["line"]["id"].split(":")[-1]
        expected = datetime.datetime.fromisoformat(dep["expectedArrivalTime"].replace("Z", "+00:00"))
        diff = int((expected - now).total_seconds() / 60)
        when = "nå" if diff <= 0 else f"{diff} min"
        print(f"  {line:<4} {front:<20} → {when}")


def show_departures():
    calls = fetch_departures()
    sentrum
