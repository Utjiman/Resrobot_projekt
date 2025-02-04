from fuzzywuzzy import fuzz

from backend.connect_to_api import ResRobot


class Stops:
    def __init__(self, resrobot: ResRobot):
        self.resrobot = resrobot

    def search_stop_by_name(self, location, threshold=80):

        # Hämta alla stop locations från ResRobot
        all_data = self.resrobot.get_location_info(location)

        # Extrahera stop locations från API:ts JSON-struktur
        stop_locations = all_data.get("stopLocationOrCoordLocation", [])

        if not stop_locations:
            return []

        matched_locations = []

        # Loopar igenom alla hittade hållplatser och kör fuzzy matchning
        for stop in stop_locations:
            stop_data = stop.get("StopLocation", {})  # Hämta StopLocation-objektet
            stop_name = stop_data.get("name", "")

            if stop_name:
                score = fuzz.partial_ratio(location.lower(), stop_name.lower())

                # Om fuzzy score är över tröskeln, inkludera hållplatsen i resultatet
                if score >= threshold:
                    matched_locations.append(
                        {
                            "name": stop_name,
                            "extId": stop_data.get("extId", "Unknown"),
                            "score": score,  # Lägg till matchningspoäng för debugging
                        }
                    )

        # Sortera resultaten efter bästa matchning (högsta score först)
        matched_locations.sort(key=lambda x: x["score"], reverse=True)

        return matched_locations

    def get_stop_info(self, ext_id: str):
        """
        Gets info about specific stop
        """
        data = self.resrobot.get_location_info(ext_id)
        stop_data = data["stopLocationOrCoordLocation"][0]["StopLocation"]
        return {
            "name": stop_data["name"],
            "lat": stop_data["lat"],
            "lon": stop_data["lon"],
            "products": stop_data["products"],
        }

    def find_nearby_stops(self, lat: float, lon: float, radius: int = 1000):
        """
        Finds nearby stops
        """
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
