from fuzzywuzzy import fuzz

from backend.connect_to_api import ResRobot


class Stops:
    """
    Stops interacts with the ResRobot API to retrieve stop information and
    depends on the ResRobot API wrapper and the fuzzywuzzy library for name matching.
    It provides three main functions:

    - Searches for stops based on a given name using fuzzy matching.
    - Retrieves detailed information about a specific stop using its external ID.
      Returns the stop's name, latitude, longitude, and available transport products.
    - Finds public transport stops within a given radius (default: 1000 meters) from
      specified coordinates.
    """

    def __init__(self, resrobot: ResRobot):
        """
        Initializes Stops with a ResRobot instance.
        """
        self.resrobot = resrobot

    def search_stop_by_name(self, location, threshold=80):
        all_data = self.resrobot.get_location_info(location)
        stop_locations = all_data.get("stopLocationOrCoordLocation", [])

        if not stop_locations:
            return []

        matched_locations = []

        for stop in stop_locations:
            stop_data = stop.get("StopLocation", {})
            stop_name = stop_data.get("name", "")

            if stop_name:
                score = fuzz.partial_ratio(location.lower(), stop_name.lower())

                if score >= threshold:
                    matched_locations.append(
                        {
                            "name": stop_name,
                            "extId": stop_data.get("extId", "Unknown"),
                            "score": score,
                        }
                    )

        matched_locations.sort(key=lambda x: x["score"], reverse=True)
        return matched_locations

    def get_stop_info(self, ext_id: str):
        data = self.resrobot.get_location_info(ext_id)
        stop_data = data["stopLocationOrCoordLocation"][0]["StopLocation"]
        return {
            "name": stop_data["name"],
            "lat": stop_data["lat"],
            "lon": stop_data["lon"],
            "products": stop_data["products"],
        }

    def find_nearby_stops(self, lat: float, lon: float, radius: int = 1000):
        data = self.resrobot.get_nearby_stops(lat, lon, radius)
        return [
            {
                "name": stop["StopLocation"]["name"],
                "lat": stop["StopLocation"]["lat"],
                "lon": stop["StopLocation"]["lon"],
                "dist": stop["StopLocation"]["dist"],
                "products": stop["StopLocation"]["products"],
            }
            for stop in data.get("stopLocationOrCoordLocation")
        ]
