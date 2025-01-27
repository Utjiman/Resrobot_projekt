from backend.connect_to_api import ResRobot


class Stops:
    def __init__(self, resrobot: ResRobot):
        self.resrobot = resrobot

    def Search_stop_by_name():
        pass

    def get_stop_info(self, ext_id: str):
        """
        Gets info about a specific stop
        """
        data = self.resrobot.access_id_from_location(ext_id)
        stop_data = data.get("stopLocationOrCoordLocation", [])
        if stop_data:
            stop_details = next(iter(stop_data[0].values()))
            return {
                "name": stop_details.get("name"),
                "lat": stop_details.get("lat"),
                "lon": stop_details.get("lon"),
                "products": stop_details.get("products"),
            }
        return None

    def find_nearby_stops(self, lat: float, lon: float, radius: int = 1000):
        """
        Finds nearby stops based on coordinates and radius
        """
        data = self.resrobot.get_nearby_stops(lat, lon, radius)
        nearby_stops = [
            {
                "name": stop["StopLocation"]["name"],
                "lat": stop["StopLocation"]["lat"],
                "lon": stop["StopLocation"]["lon"],
                "dist": stop["StopLocation"]["dist"],
                "products": stop["StopLocation"]["products"],
            }
            for stop in data.get("stopLocationOrCoordLocation", [])
        ]
        return nearby_stops
