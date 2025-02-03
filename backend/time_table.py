from datetime import datetime

from backend.connect_to_api import ResRobot


class TimeTable:

    def __init__(self, resrobot: ResRobot):
        self.resrobot = resrobot

    def show_departure_from_stop(self, stop_id: int):
        """
        Show departures from a specific stop
        """
        data = self.resrobot.get_timetable(
            location_id=stop_id
        )  # Gets data from resrobot
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
                continue  # Skip if time is not available

            # Parse departure time to datetime
            departure_time = datetime.strptime(departure_time_str, "%H:%M:%S").replace(
                year=now.year, month=now.month, day=now.day
            )

            # Calculate time remaining in minutes
            time_remaining = int((departure_time - now).total_seconds() // 60)
            if time_remaining >= 0:  # Only include future departures
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
