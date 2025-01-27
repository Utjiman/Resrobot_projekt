from backend.connect_to_api import ResRobot
from backend.time_table import TimeTable
from backend.trips import TripPlanner


def main():

    resrobot = ResRobot()
    timetable = TimeTable(resrobot)

    origin_id = 740000195  # Sandviken Station
    stop_id = 740000002  # Göteborg Centralstation

    departures = timetable.show_departure_from_stop(stop_id)
    trip_planner = TripPlanner(origin_id, stop_id)
    trips_today = trip_planner.next_available_trips_today()

    print("show_departure_from_stop: Göteborg Centralstation")
    for dep in departures[:10]:  # 10 first
        print(dep)

    print("5 first trips today: Sandviken Station - Göteborg Centralstation")
    for trip in trips_today[:5]:
        print(trip)


if __name__ == "__main__":
    main()
