from backend.connect_to_api import ResRobot
from backend.time_table import TimeTable


def main():

    resrobot = ResRobot()
    timetable = TimeTable(resrobot)

    stop_id = 740000002  # Göteborg Centralstation
    departures = timetable.show_departure_from_stop(stop_id)

    print("show_departure_from_stop: Göteborg Centralstation")
    for dep in departures[:10]:  # 10 first
        print(dep)


if __name__ == "__main__":
    main()
