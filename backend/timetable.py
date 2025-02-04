from datetime import datetime

from backend.connect_to_api import ResRobot


class TimeTable:
    """
    The TimeTable class interacts with the ResRobot API to retrieve departure
    times from a given stop. This class relies on the ResRobot API for
    timetable data and uses Python's datetime module to process time calculations.

    Features:
    - Fetches all departures from a specific stop using its ID.
    - Calculates the time remaining (in minutes) until each departure from a given
      stop. Only includes upcoming departures and sorts them by soonest departure.
    - Retrieves departures within the next hour from a given stop.
    """

    def __init__(self, resrobot: ResRobot):
        """
        Initializes TimeTable with a ResRobot instance.
        """
        self.resrobot = resrobot

    def show_departure_from_stop(self, stop_id: int):
        data = self.resrobot.get_timetable(location_id=stop_id)

        departures = data.get("Departure", [])

        result = []
        for departure in departures:
            line = departure.get("ProductAtStop", {}).get("name", "Okänd linje")
            direction = departure.get("direction", "Okänd destination")
            time = departure.get("time", "N/A")
            result.append({"Linje": line, "Destination": direction, "Avgångstid": time})

        return result

    def show_time_to_departure(self, stop_id: int, limit: int = 20):
        data = self.resrobot.get_timetable(location_id=stop_id)
        departures = data.get("Departure", [])

        now = datetime.now()
        result = []

        for departure in departures:
            line = departure.get("ProductAtStop", {}).get("name", "Okänd linje")
            direction = departure.get("direction", "Okänd destination")
            departure_time_str = departure.get("time", None)

            if not departure_time_str:
                continue

            departure_time = datetime.strptime(departure_time_str, "%H:%M:%S").replace(
                year=now.year, month=now.month, day=now.day
            )

            time_remaining = int((departure_time - now).total_seconds() // 60)
            if time_remaining >= 0:
                result.append(
                    {
                        "Linje": line,
                        "Destination": direction,
                        "Tid kvar (min)": time_remaining,
                    }
                )

        return sorted(result, key=lambda x: x["Tid kvar (min)"])[:limit]

    def show_one_hour_ahead(self, stop_id: int):
        data = self.resrobot.get_timetable(location_id=stop_id)
        departures = data.get("Departure", [])

        now = datetime.now()
        result = []

        for departure in departures:
            line = departure.get("ProductAtStop", {}).get("name", "Okänd linje")
            direction = departure.get("direction", "Okänd destination")
            departure_time_str = departure.get("time", None)

            if not departure_time_str:
                continue

            departure_time = datetime.strptime(departure_time_str, "%H:%M:%S").replace(
                year=now.year, month=now.month, day=now.day
            )

            time_remaining = int((departure_time - now).total_seconds() // 60)
            if time_remaining >= 0:
                result.append(
                    {
                        "Linje": line,
                        "Destination": direction,
                        "Tid kvar (min)": time_remaining,
                    }
                )

        return sorted(result, key=lambda x: x["Tid kvar (min)"])
