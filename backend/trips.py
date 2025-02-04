from datetime import datetime

import folium
import pandas as pd

from backend.connect_to_api import ResRobot

resrobot = ResRobot()


class TripPlanner:
    """
    A class to interact with Resrobot API to plan trips and retrieve details of available journeys.

    Check explorations to find id for your location

    Attributes:
    ----------
    trips : list
        A list of trips retrieved from the Resrobot API for the specified origin and destination.
    number_trips : int
        The total number of trips available for the specified origin and destination.

    Methods:
    -------
    next_available_trip() -> pd.DataFrame:
        Returns a DataFrame containing details of the next available trip, including stop names,
        coordinates, departure and arrival times, and dates.
    next_available_trips_today() -> list[pd.DataFrame]
        Returns a list of DataFrame objects, where each DataFrame contains similar content as next_available_trip()
    """

    def __init__(self, origin_id, destination_id) -> None:
        self.origin_id = origin_id
        self.destination_id = destination_id
        response = resrobot.trips(origin_id, destination_id)
        # Ensure self.trips is a list; if the API response is empty, set an empty list.
        self.trips = response.get("Trip", []) if response else []

    def next_available_trip(self) -> pd.DataFrame:
        if not self.trips:
            return pd.DataFrame()

        next_trip = self.trips[0]
        # Safely retrieve the list of legs; use an empty list if missing
        leglist = next_trip.get("LegList", {}).get("Leg", [])
        stops_list = []

        # Loop over each leg and extract stop data safely
        for leg in leglist:
            stops_container = leg.get("Stops", {})
            stops = stops_container.get("Stop")
            if stops:
                if isinstance(stops, list):
                    stops_list.extend(stops)
                else:
                    stops_list.append(stops)

        if not stops_list:
            # Return an empty DataFrame if no stop data is available
            print("Not enough data available to generate trip information.")
            return pd.DataFrame()

        df_stops = pd.DataFrame(stops_list)

        if "arrTime" in df_stops.columns or "depTime" in df_stops.columns:
            df_stops["time"] = df_stops.get("arrTime").fillna(df_stops.get("depTime"))
        else:
            df_stops["time"] = "Not available"

        if "arrDate" in df_stops.columns or "depDate" in df_stops.columns:
            df_stops["date"] = df_stops.get("arrDate").fillna(df_stops.get("depDate"))
        else:
            df_stops["date"] = "Not available"

        required_cols = [
            "name",
            "extId",
            "lon",
            "lat",
            "depTime",
            "depDate",
            "arrTime",
            "arrDate",
            "time",
            "date",
        ]
        for col in required_cols:
            if col not in df_stops.columns:
                df_stops[col] = "Not available"

        return df_stops[required_cols]

    def next_available_trips_today(self) -> list[pd.DataFrame]:
        trips_today = []
        today = pd.Timestamp("today").strftime("%Y-%m-%d")

        for trip in self.trips:
            leglist = trip.get("LegList", {}).get("Leg", [])
            stops_list = []
            for leg in leglist:
                stops_container = leg.get("Stops", {})
                stops = stops_container.get("Stop")
                if stops:
                    if isinstance(stops, list):
                        stops_list.extend(stops)
                    else:
                        stops_list.append(stops)

            if not stops_list:
                continue

            df_stops = pd.DataFrame(stops_list)
            if "arrTime" in df_stops.columns or "depTime" in df_stops.columns:
                df_stops["time"] = df_stops.get("arrTime").fillna(
                    df_stops.get("depTime")
                )
            else:
                df_stops["time"] = "Not available"
            if "arrDate" in df_stops.columns or "depDate" in df_stops.columns:
                df_stops["date"] = df_stops.get("arrDate").fillna(
                    df_stops.get("depDate")
                )
            else:
                df_stops["date"] = "Not available"

            if (
                "date" in df_stops.columns
                and df_stops["date"].str.contains(today).any()
            ):
                required_cols = [
                    "name",
                    "extId",
                    "lon",
                    "lat",
                    "depTime",
                    "depDate",
                    "arrTime",
                    "arrDate",
                    "time",
                    "date",
                ]
                for col in required_cols:
                    if col not in df_stops.columns:
                        df_stops[col] = "Not available"
                trips_today.append(df_stops[required_cols])

        return trips_today

    def calc_number_of_stops(self, trip_index=0):
        if not self.trips or trip_index >= len(self.trips):
            return 0

        selected_trip = self.trips[trip_index]
        total_stops = 0
        for leg in selected_trip.get("LegList", {}).get("Leg", []):
            stops = leg.get("Stops", {}).get("Stop")
            if stops:
                if isinstance(stops, list):
                    total_stops += len(stops)
                else:
                    total_stops += 1
        return total_stops

    def calc_number_of_changes(self, trip_index=0):
        if not self.trips or trip_index >= len(self.trips):
            return 0

        selected_trip = self.trips[trip_index]
        # default to an empty list if missing
        number_of_legs = len(selected_trip.get("LegList", {}).get("Leg", []))
        number_of_changes = max(0, number_of_legs - 1)
        return number_of_changes

    def calc_total_time(self, trip_index=0):
        if not self.trips:
            return "No trips found"

        selected_trip = self.trips[trip_index]
        legs = selected_trip.get("LegList", {}).get("Leg", [])
        if not legs:
            return "No time data available"

        first_leg = legs[0]
        last_leg = legs[-1]
        departure_time = f"{first_leg['Origin']['date']} {first_leg['Origin']['time']}"
        arrival_time = (
            f"{last_leg['Destination']['date']} {last_leg['Destination']['time']}"
        )
        fmt = "%Y-%m-%d %H:%M:%S"
        duration = datetime.strptime(arrival_time, fmt) - datetime.strptime(
            departure_time, fmt
        )
        return str(duration).split(".")[0]

    def map_for_trip(self, trip_index=0):
        if not self.trips or trip_index >= len(self.trips):
            print("No valid trip found.")
            return None

        selected_trip = self.trips[trip_index]
        stops_data = []
        # Loop through each leg and process stop data
        for leg in selected_trip.get("LegList", {}).get("Leg", []):
            stops = leg.get("Stops", {}).get("Stop")
            if stops:
                if not isinstance(stops, list):
                    stops = [stops]
                for stop in stops:
                    stop_data = {
                        "name": stop.get("name", "Unknown"),
                        "lat": float(stop.get("lat", 0)),
                        "lon": float(stop.get("lon", 0)),
                        "arr_time": stop.get("arrTime", "Not available"),
                        "dep_time": stop.get("depTime", "Not available"),
                    }
                    stops_data.append(stop_data)

        if not stops_data:
            print("No stops data found.")
            return None

        df_stops = pd.DataFrame(stops_data)
        # Create a map centered on the average latitude and longitude
        map_center = [df_stops["lat"].mean(), df_stops["lon"].mean()]
        trip_map = folium.Map(location=map_center, zoom_start=6)

        # Add markers for each stop
        for _, row in df_stops.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=f"<b>{row['name']}</b><br>Arr: {row['arr_time']}<br>Dep: {row['dep_time']}",
                icon=folium.Icon(color="blue"),
            ).add_to(trip_map)

        return trip_map
