import os
from abc import ABC, abstractmethod

import folium
import requests
import streamlit as st
from dotenv import load_dotenv

from backend.trips import TripPlanner

load_dotenv()
API_KEY = os.getenv("API_KEY")


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
    """Hämtar koordinater för en hållplats baserat på extId."""
    url = f"https://api.resrobot.se/v2.1/location.name?input={ext_id}&format=json&accessId={API_KEY}"
    result = requests.get(url).json()

    for stop in result.get("stopLocationOrCoordLocation", []):
        stop_data = list(stop.values())[0]
        return {
            "name": stop_data.get("name"),
            "lat": stop_data.get("lat"),
            "lon": stop_data.get("lon"),
        }
    return None


def get_nearby_stops(ext_id, radius=1000):
    """Hämtar närliggande hållplatser inom en given radie."""

    # Hämta huvudhållplatsens koordinater och namn
    base_url = f"https://api.resrobot.se/v2.1/location.name?input={ext_id}&format=json&accessId={API_KEY}"
    base_data = next(
        iter(requests.get(base_url).json()["stopLocationOrCoordLocation"][0].values())
    )

    # Hämta närliggande hållplatser
    nearby_url = f"https://api.resrobot.se/v2.1/location.nearbystops?originCoordLat={base_data['lat']}&originCoordLong={base_data['lon']}&r={radius}&format=json&accessId={API_KEY}"
    nearby_stops = [
        {
            "name": stop["StopLocation"]["name"],
            "lat": float(stop["StopLocation"]["lat"]),
            "lon": float(stop["StopLocation"]["lon"]),
        }
        for stop in requests.get(nearby_url).json()["stopLocationOrCoordLocation"]
    ]

    return {
        "base": {
            "name": base_data["name"],
            "lat": float(base_data["lat"]),
            "lon": float(base_data["lon"]),
        },
        "nearby_stops": nearby_stops,
    }


def create_map_with_stops(data):
    """Skapar en Folium-karta med närliggande hållplatser."""
    map_obj = folium.Map(
        location=[data["base"]["lat"], data["base"]["lon"]], zoom_start=14
    )

    # Lägg till huvudhållplatsen (röd)
    folium.Marker(
        [data["base"]["lat"], data["base"]["lon"]],
        popup=f"Huvudhållplats: {data['base']['name']}",
        icon=folium.Icon(color="red"),
    ).add_to(map_obj)

    # Lägg till närliggande hållplatser (blåa)
    for stop in data["nearby_stops"]:
        if (
            stop["name"] == data["base"]["name"]
            and stop["lat"] == data["base"]["lat"]
            and stop["lon"] == data["base"]["lon"]
        ):
            continue
        folium.Marker(
            [stop["lat"], stop["lon"]],
            popup=f"Närliggande hållplats: {stop['name']}",
            icon=folium.Icon(color="blue"),
        ).add_to(map_obj)

    return map_obj
