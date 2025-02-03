from datetime import datetime

import pandas as pd
import requests

from backend.connect_to_api import ResRobot


class ResRobotDay:
    """
    This Python class fetches today's departures and arrivals
    from the ResRobot API, covering the time range from
    midnight to the current moment. However, the API only
    retains data for a few hours, meaning it does not provide
    historical data beyond 5-6 hours.
    """

    def __init__(self):
        self.res = ResRobot()
        self.API_KEY = self.res.api_key

    def departures_until_now(self, station_id: int) -> pd.DataFrame:
        """
        Fetches departures (departureBoard) from midnight until now (today's date).
        """
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")

        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        minutes_since_midnight = int((now - midnight).total_seconds() / 60)

        url = "https://api.resrobot.se/v2.1/departureBoard"
        params = {
            "id": station_id,
            "format": "json",
            "accessId": self.API_KEY,
            "date": date_str,
            "time": "00:00",
            "duration": minutes_since_midnight,
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
        Fetches arrivals (arrivalBoard) from midnight until now (today's date).
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
            "duration": minutes_since_midnight,
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
