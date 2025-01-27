from backend.connect_to_api import ResRobot


class Stops:
    def __init__(self, resrobot: ResRobot):
        self.resrobot = resrobot

    def Search_stop_by_name():
        pass

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
