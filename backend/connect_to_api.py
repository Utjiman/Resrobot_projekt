import requests
import streamlit as st


class ResRobot:
    """
    A Python client for interacting with the ResRobot API.

    This class provides methods to retrieve public transport data such as trips,
    location details, timetables, and nearby stops using the ResRobot API.

    Features:
    - Fetch trip details between two locations.
    - Retrieve location information based on a place name.
    - Get departure and arrival timetables for a specific stop.
    - Find nearby stops based on GPS coordinates.

    API key is required and should be stored in `secrets.toml`.
    """

    def __init__(self, api_key=None):
        """Initializes ResRobot with an API key."""
        self.api_key = api_key or st.secrets["api"]["API_KEY"]

        if not self.api_key:
            raise ValueError(
                "API_KEY is missing! Make sure it is defined in the secrets.toml file."
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

    def get_location_info(self, location):
        url = (
            f"https://api.resrobot.se/v2.1/location.name?"
            f"input={location}&format=json&accessId={self.api_key}"
        )
        return self._make_request(url)

    def get_timetable(self, location_id, board_type="departure"):
        endpoint = "departureBoard" if board_type == "departure" else "arrivalBoard"
        url = (
            f"https://api.resrobot.se/v2.1/{endpoint}?"
            f"id={location_id}&format=json&accessId={self.api_key}"
        )
        return self._make_request(url)

    def get_nearby_stops(self, lat, lon, radius=1000):
        url = (
            f"https://api.resrobot.se/v2.1/location.nearbystops?"
            f"originCoordLat={lat}&originCoordLong={lon}&r={radius}"
            f"&format=json&accessId={self.api_key}"
        )
        return self._make_request(url)
