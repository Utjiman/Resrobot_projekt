from backend.connect_to_api import ResRobot


class Stops:
    def __init__(self, resrobot: ResRobot):
        self.resrobot = resrobot

    def search_stop_by_name(self, location):

        # Hämta alla stop locations från API:et
        all_locations = self.resrobot.access_id_from_location(location)
        # 🛠 Debugging för att se strukturen

        # Kontrollera att vi har fått en giltig respons
        if not all_locations or "stopLocationOrCoordLocation" not in all_locations:
            return []

        # Hämta listan med stopp
        stop_locations = all_locations["stopLocationOrCoordLocation"]

        matched_locations = []
        for stop in stop_locations:
            stop_data = stop.get("StopLocation", {})  # 🔹 Hämta StopLocation-objektet
            stop_name = stop_data.get("name", "")

            if stop_name:  # Se till att stop_name finns
                matched_locations.append({"name": stop_name})

        return matched_locations

    def get_stop_info(self, ext_id: str):
        """
        Gets info about specific stop
        """
        data = self.resrobot.get_stop_details(ext_id)
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
            for stop in data["stopLocationOrCoordLocation"]
        ]


# Skapa instans av ResRobot
