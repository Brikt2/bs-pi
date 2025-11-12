import requests
import datetime
import time
import os

ENTUR_URL = "https://api.entur.io/journey-planner/v3/graphql"
STOP_PLACE_ID = "NSR:StopPlace:6435"

SENTRUM = ["Kværnerbyen", "Ekeberg hageby"]
OTHER_WAY = ["Kjelsås stasjon", "Tåsen"]

QUERY = """
{
  stopPlace(id: "%s") {
    id
    name
    estimatedCalls(timeRange: 72100, numberOfDepartures: 12) {
      realtime
      aimedArrivalTime
      expectedArrivalTime
      destinationDisplay {
      frontText
      }
      serviceJourney {
        journeyPattern {
          line {
            id
            transportMode
          }
        }
      }
    }
  }
}
""" % STOP_PLACE_ID


def fetch_departures():
    try:
        response = requests.post(
            ENTUR_URL,
            headers={
                "Content-Type": "application/json",
                "ET-Client-Name": "Infoboard-app",
            },
            json={"query": QUERY},
        )
        response.raise_for_status()
        return response.json()["data"]["stopPlace"]["estimatedCalls"]
    except Exception as e:
        print("Feil ved henting av data:", e)
        return []


def show_departures(calls):
    sentrum_departures = []
    other_way_departures = []

    for call in calls:
        front_text = call["destinationDisplay"]["frontText"]
        if front_text in SENTRUM:
            sentrum_departures.append(call)
        elif front_text in OTHER_WAY:
            other_way_departures.append(call)

    print("\n=== Retning sentrum ===")
    print_departures(sentrum_departures)

    print("\n=== Gokk ===")
    print("\n=== Gakk ===")
    print_departures(other_way_departures)


def print_departures(departures):
    now = datetime.datetime.now(datetime.timezone.utc)
    for dep in departures:
        front_text = dep["destinationDisplay"]["frontText"]
        line_id = dep["serviceJourney"]["journeyPattern"]["line"]["id"].split(":")[-1]
        expected_time = datetime.datetime.fromisoformat(dep["expectedArrivalTime"].replace("Z", "+00:00"))
        minutes = int((expected_time - now).total_seconds() / 60)
        minutes_display = "nå" if minutes <= 0 else f"{minutes} min"
        print(f"{line_id} {front_text:20s}  →  {minutes_display}")


if __name__ == "__main__":
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print("🚌 Henter bussavganger fra Entur...")
        calls = fetch_departures()
        show_departures(calls)
        time.sleep(30)
