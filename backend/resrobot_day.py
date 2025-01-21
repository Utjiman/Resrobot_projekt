import pandas as pd
from datetime import datetime
import requests

from backend.connect_to_api import ResRobot

class ResRobotDay:
    """
    Hämtar dagens avgångar och ankomster från midnatt till nu, 
    API:et sparar bara data några timmar tillbaka så man får inte
    data för mer än 5-6 timmar bakåt i tiden.
    """

    def __init__(self):
        # Skapa en instans av ResRobot
        self.res = ResRobot()
        # Återanvänd API_KEY
        self.API_KEY = self.res.API_KEY

    def departures_until_now(self, station_id: int) -> pd.DataFrame:
        """
        Hämtar avgångar (departureBoard) från midnatt fram till nu (dagens datum).
        """
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")

        # Beräkna minuter sedan midnatt
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        minutes_since_midnight = int((now - midnight).total_seconds() / 60)

        url = "https://api.resrobot.se/v2.1/departureBoard"
        params = {
            "id": station_id,
            "format": "json",
            "accessId": self.API_KEY,
            "date": date_str,          # dagens datum
            "time": "00:00",           # från midnatt
            "duration": minutes_since_midnight
        }
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            departures = data.get("Departure", [])
            return pd.DataFrame(departures)
        except requests.exceptions.RequestException as err:
            print(f"HTTP-fel vid hämtning av avgångar: {err}")
            return pd.DataFrame()

    def arrivals_until_now(self, station_id: int) -> pd.DataFrame:
        """
        Hämtar ankomster (arrivalBoard) från midnatt fram till nu (dagens datum).
        """
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")

        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        minutes_since_midnight = int((now - midnight).total_seconds() / 60)

        url = "https://api.resrobot.se/v2.1/arrivalBoard"
        params = {
            "id": station_id,
            "format": "json",
            "accessId": self.API_KEY,
            "date": date_str,
            "time": "00:00",
            "duration": minutes_since_midnight
        }
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            arrivals = data.get("Arrival", [])
            return pd.DataFrame(arrivals)
        except requests.exceptions.RequestException as err:
            print(f"HTTP-fel vid hämtning av ankomster: {err}")
            return pd.DataFrame()
        

