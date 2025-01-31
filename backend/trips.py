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
        self.trips = resrobot.trips(origin_id, destination_id).get("Trip")

    def next_available_trip(self) -> pd.DataFrame:
        next_trip = self.trips[0]

        leglist = next_trip.get("LegList").get("Leg")

        df_legs = pd.DataFrame(leglist)

        df_stops = pd.json_normalize(df_legs["Stops"].dropna(), "Stop", errors="ignore")

        df_stops["time"] = df_stops["arrTime"].fillna(df_stops["depTime"])
        df_stops["date"] = df_stops["arrDate"].fillna(df_stops["depDate"])

        return df_stops[
            [
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
        ]

    def next_available_trips_today(self) -> list[pd.DataFrame]:
        """Fetches all available trips today between the origin_id and destination_id
        It returns a list of DataFrame objects, where each item corresponds to a trip
        """
        trips_today = []
        today = pd.Timestamp("today").strftime("%Y-%m-%d")

        for trip in self.trips:
            leglist = trip.get("LegList").get("Leg")
            df_legs = pd.DataFrame(leglist)

            df_stops = pd.json_normalize(
                df_legs["Stops"].dropna(), "Stop", errors="ignore"
            )
            df_stops["time"] = df_stops["arrTime"].fillna(df_stops["depTime"])
            df_stops["date"] = df_stops["arrDate"].fillna(df_stops["depDate"])

            if (df_stops["date"].str.contains(today)).any():
                trips_today.append(
                    df_stops[
                        [
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
                    ]
                )

        return trips_today

    def calc_number_of_stops(self, trip_index=0):
        """
        Calculates the total number of stops for the trip.
        """
        selected_trip = self.trips[
            trip_index
        ]  # Selects a specific trip based on trip_index
        total_stops = sum(
            len(leg["Stops"]["Stop"]) for leg in selected_trip["LegList"]["Leg"]
        )  # Counts the total number of stops by summing up the stops in each leg of the trip
        return total_stops

    def calc_number_of_changes(self, trip_index=0):
        """
        Calculates the number of changes (transfers) during the trip.
        """

        selected_trip = self.trips[trip_index]
        number_of_legs = len(
            selected_trip["LegList"]["Leg"]
        )  # Count the number of legs
        number_of_changes = max(
            0, number_of_legs - 1
        )  # Calculate transfers (minimum 0),
        # Changes = legs - 1 (e.g., 3 legs → 2 changes)

        return number_of_changes

    def calc_total_time(self, trip_index=0):
        """Calculates the total travel time for the trip in HH:MM format."""

        if not self.trips:
            return "No trips found"

        # Select the specified trip
        selected_trip = self.trips[trip_index]

        # Extract first departure and last arrival times
        first_leg = selected_trip["LegList"]["Leg"][0]
        last_leg = selected_trip["LegList"]["Leg"][-1]

        departure_time = f"{first_leg['Origin']['date']} {first_leg['Origin']['time']}"
        arrival_time = (
            f"{last_leg['Destination']['date']} {last_leg['Destination']['time']}"
        )

        # Convert and calculate duration
        fmt = "%Y-%m-%d %H:%M:%S"
        duration = datetime.strptime(arrival_time, fmt) - datetime.strptime(
            departure_time, fmt
        )

        # Return total travel time in HH:MM format
        return str(duration).split(".")[0]

    def map_for_trip(self, trip_index=0):

        if not self.trips or trip_index >= len(self.trips):
            print("No valid trip found.")
            return None

        selected_trip = self.trips[trip_index]
        stops_data = []

        # Hämta alla stopp från alla legs
        for leg in selected_trip["LegList"]["Leg"]:
            stops = leg.get("Stops", {}).get("Stop", [])
            for stop in stops:
                stop_data = {
                    "name": stop.get("name"),
                    "lat": float(stop.get("lat", 0)),
                    "lon": float(stop.get("lon", 0)),
                    "arr_time": stop.get("arrTime"),
                    "dep_time": stop.get("depTime"),
                }
                stops_data.append(stop_data)

        if not stops_data:
            print("No stops data found.")
            return None

        df_stops = pd.DataFrame(stops_data)

        # Skapa en karta centrerad på medelvärdet av alla koordinater
        map_center = [df_stops["lat"].mean(), df_stops["lon"].mean()]
        trip_map = folium.Map(location=map_center, zoom_start=6)

        # Lägg till markörer för varje stopp
        for _, row in df_stops.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=f"<b>{row['name']}</b><br>Arr: {row['arr_time']}<br>Dep: {row['dep_time']}",
                icon=folium.Icon(color="blue"),
            ).add_to(trip_map)

        return trip_map
