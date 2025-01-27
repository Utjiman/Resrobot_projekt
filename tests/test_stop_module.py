from backend.connect_to_api import ResRobot
from backend.stop_module import Stops


def main():
    resrobot = ResRobot()
    stops = Stops(resrobot)

    ext_id = 740000002  # Göteborg Centralstation
    stop_info = stops.get_stop_info(ext_id)
    print("\nDetaljer för hållplats (get_stop_info):")
    print(stop_info)

    lat, lon = 57.708895, 11.973479  # Göteborg Centralstation
    nearby_stops = stops.find_nearby_stops(lat, lon, radius=500)

    print("\nNärliggande hållplatser (find_nearby_stops):")
    for stop in nearby_stops[:5]:
        print(stop)


if __name__ == "__main__":
    main()
