from abc import ABC, abstractmethod

import folium
import streamlit as st

from backend.connect_to_api import ResRobot
from backend.trips import TripPlanner

"""
Module for handling map-related operations in the application.
This module provides functionality for visualizing transport routes.
and nearby stops using Folium maps. It includes an abstract base class
for map operations and implementations for trip maps and nearby stop maps.

Features:
- Abstract base class `Maps` for defining map display behavior.
- `TripMap` class for visualizing planned trips on a map.
- Functions for retrieving coordinates and nearby stops via ResRobot API.
- Functions for generating interactive Folium maps with stop markers.
"""

api_client = ResRobot()


class Maps(ABC):
    """
    Abstract base class for map-related operations.

    Methods:
    --------
    display_map():
        Abstract method to display a map. Must be implemented by subclasses.
    """

    @abstractmethod
    def display_map(self):
        """
        Abstract method to display a map.

        Subclasses must provide an implementation for this method.
        """
        raise NotImplementedError


class TripMap(Maps):
    def __init__(self, origin_id, destination_id):
        trip_planner = TripPlanner(origin_id, destination_id)
        self.next_trip = trip_planner.next_available_trip()

    def _create_map(self):
        geographical_map = folium.Map(
            location=[self.next_trip["lat"].mean(), self.next_trip["lon"].mean()],
            zoom_start=5,
        )

        for _, row in self.next_trip.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=f"{row['name']}<br>{row['time']}<br>{row['date']}",
            ).add_to(geographical_map)

        return geographical_map

    def display_map(self):
        st.markdown("## Karta över stationerna i din resa")
        st.markdown(
            "Klicka på varje station för mer information. Detta är en exempelresa mellan Malmö och Umeå"
        )
        st.components.v1.html(self._create_map()._repr_html_(), height=500)


def get_coordinates_from_extid(ext_id):

    stop_data = api_client.get_location_info(ext_id)

    if not stop_data or "stopLocationOrCoordLocation" not in stop_data:
        return None

    for stop in stop_data["stopLocationOrCoordLocation"]:
        stop_info = list(stop.values())[0]
        return {
            "name": stop_info.get("name"),
            "lat": float(stop_info.get("lat")),
            "lon": float(stop_info.get("lon")),
        }
    return None


def get_nearby_stops(ext_id, radius=1000):

    base_stop = get_coordinates_from_extid(ext_id)

    if not base_stop:
        return None

    nearby_stops = api_client.get_nearby_stops(
        base_stop["lat"], base_stop["lon"], radius
    )

    if not nearby_stops or "stopLocationOrCoordLocation" not in nearby_stops:
        return None

    stop_list = [
        {
            "name": stop["StopLocation"]["name"],
            "lat": float(stop["StopLocation"]["lat"]),
            "lon": float(stop["StopLocation"]["lon"]),
        }
        for stop in nearby_stops["stopLocationOrCoordLocation"]
    ]

    return {
        "base": base_stop,
        "nearby_stops": stop_list,
    }


def create_map_with_stops(data):

    map_obj = folium.Map(
        location=[data["base"]["lat"], data["base"]["lon"]], zoom_start=14
    )

    folium.Marker(
        [data["base"]["lat"], data["base"]["lon"]],
        popup=f"Huvudhållplats: {data['base']['name']}",
        icon=folium.Icon(color="red"),
    ).add_to(map_obj)

    for stop in data["nearby_stops"]:
        if stop["name"] == data["base"]["name"]:
            continue
        folium.Marker(
            [stop["lat"], stop["lon"]],
            popup=f"Närliggande hållplats: {stop['name']}",
            icon=folium.Icon(color="blue"),
        ).add_to(map_obj)

    return map_obj
