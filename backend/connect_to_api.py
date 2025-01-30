import os

import requests
from dotenv import load_dotenv

load_dotenv()


class ResRobot:
    """ResRobot API client for API requests."""

    def __init__(self, api_key=None):
        """Initializes ResRobot with an API key."""
        self.api_key = api_key or os.getenv("API_KEY")

        if not self.api_key:
            raise ValueError(
                "API_KEY is missing! Make sure it is defined in the .env file."
            )

    def _make_request(self, url: str):
        """Private method to send HTTP requests and handle errors."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(f"Network or HTTP error: {err}")
            return None

    def trips(self, origin_id, destination_id):
        url = (
            f"https://api.resrobot.se/v2.1/trip?"
            f"format=json&originId={origin_id}&destId={destination_id}"
            f"&passlist=true&showPassingPoints=true&accessId={self.api_key}"
        )
        return self._make_request(url)

    def access_id_from_location(self, location):
        url = (
            f"https://api.resrobot.se/v2.1/location.name?"
            f"input={location}&format=json&accessId={self.api_key}"
        )
        return self._make_request(url)

    def timetable_departure(self, location_id):
        url = (
            f"https://api.resrobot.se/v2.1/departureBoard?"
            f"id={location_id}&format=json&accessId={self.api_key}"
        )
        return self._make_request(url)

    def timetable_arrival(self, location_id):
        url = (
            f"https://api.resrobot.se/v2.1/arrivalBoard?"
            f"id={location_id}&format=json&accessId={self.api_key}"
        )
        return self._make_request(url)

    def get_stop_details(self, ext_id):
        url = (
            f"https://api.resrobot.se/v2.1/location.name?"
            f"input={ext_id}&format=json&accessId={self.api_key}"
        )
        return self._make_request(url)

    def get_nearby_stops(self, lat, lon, radius=1000):
        url = (
            f"https://api.resrobot.se/v2.1/location.nearbystops?"
            f"originCoordLat={lat}&originCoordLong={lon}&r={radius}"
            f"&format=json&accessId={self.api_key}"
        )
        return self._make_request(url)
