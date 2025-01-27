import os

import requests
from dotenv import load_dotenv

load_dotenv()


class ResRobot:

    API_KEY = os.getenv("API_KEY")

    def trips(self, origin_id=740000001, destination_id=740098001):
        """origing_id and destination_id can be found from Stop lookup API"""
        url = f"https://api.resrobot.se/v2.1/trip?format=json&originId={origin_id}&destId={destination_id}&passlist=true&showPassingPoints=true&accessId={self.API_KEY}"

        try:
            response = requests.get(url)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as err:
            print(f"Network or HTTP error: {err}")

    def access_id_from_location(self, location):
        url = f"https://api.resrobot.se/v2.1/location.name?input={location}&format=json&accessId={self.API_KEY}"
        response = requests.get(url)
        result = response.json()
        return result

    def timetable_departure(self, location_id=740015565):
        url = f"https://api.resrobot.se/v2.1/departureBoard?id={location_id}&format=json&accessId={self.API_KEY}"
        response = requests.get(url)
        result = response.json()
        return result

    def timetable_arrival(self, location_id=740015565):
        url = f"https://api.resrobot.se/v2.1/arrivalBoard?id={location_id}&format=json&accessId={self.API_KEY}"
        response = requests.get(url)
        result = response.json()
        return result

    def get_stop_details(self, ext_id: str):
        url = f"https://api.resrobot.se/v2.1/location.name?input={ext_id}&format=json&accessId={self.API_KEY}"
        response = requests.get(url)
        result = response.json()
        return result

    def get_nearby_stops(self, lat: float, lon: float, radius: int = 1000):
        url = f"https://api.resrobot.se/v2.1/location.nearbystops?originCoordLat={lat}&originCoordLong={lon}&r={radius}&format=json&accessId={self.API_KEY}"
        response = requests.get(url)
        result = response.json()
        return result
