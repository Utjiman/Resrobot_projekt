from backend.connect_to_api import ResRobot
from backend.time_table import TimeTable

def main():
    resrobot = ResRobot()
    timetable = TimeTable(resrobot)

    
    stop_id = 740000002

    # result = timetable.show_one_hour_ahead(stop_id) remove comment and comment out show_time_to_departure to test instead.
    result = timetable.show_time_to_departure(stop_id)

    if not result:
        print("Inga avgångar hittades.")
    else:
        print("Kommande avgångar:")
        for departure in result:
            print(
                f"Linje {departure['Linje']} mot {departure['Destination']}, "
                f"avgår om {departure['Tid kvar (min)']} minuter."
            )

if __name__ == "__main__":
    main()
