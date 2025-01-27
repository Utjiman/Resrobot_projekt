import os

import folium
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
from dotenv import load_dotenv

from backend.resrobot_day import ResRobotDay

load_dotenv()

API_KEY = os.getenv("API_KEY")


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
    """Skapar en foliumkarta med närliggande hållplatser."""
    map_obj = folium.Map(
        location=[data["base"]["lat"], data["base"]["lon"]], zoom_start=14
    )

    # Lägger till huvudhållplatsen (röd)
    folium.Marker(
        [data["base"]["lat"], data["base"]["lon"]],
        popup=f"Huvudhållplats: {data['base']['name']}",
        icon=folium.Icon(color="red"),
    ).add_to(map_obj)

    # Lägger till närliggande hållplatser (blåa)
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


def prepare_and_plot_graph(station_id):
    rr_today = ResRobotDay()

    df_dep = rr_today.departures_until_now(station_id)
    df_arr = rr_today.arrivals_until_now(station_id)

    if not df_dep.empty and "time" in df_dep.columns:
        df_dep["Hour"] = df_dep["time"].str.split(":").str[0].astype(int)
        dep_count_by_hour = df_dep["Hour"].value_counts().sort_index()
    else:
        dep_count_by_hour = pd.Series([0] * 24, index=range(24))

    if not df_arr.empty and "time" in df_arr.columns:
        df_arr["Hour"] = df_arr["time"].str.split(":").str[0].astype(int)
        arr_count_by_hour = df_arr["Hour"].value_counts().sort_index()
    else:
        arr_count_by_hour = pd.Series([0] * 24, index=range(24))

    # Kombinera data till en DataFrame
    hours = range(24)
    df_hours = pd.DataFrame(
        {
            "Hour": hours,
            "Departures": [dep_count_by_hour.get(hour, 0) for hour in hours],
            "Arrivals": [arr_count_by_hour.get(hour, 0) for hour in hours],
        }
    ).set_index("Hour")

    # Omstrukturera DataFrame till långt format för Seaborn
    df_long = df_hours.reset_index().melt(
        id_vars="Hour",
        value_vars=["Departures", "Arrivals"],
        var_name="Type",
        value_name="Count",
    )

    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 7))
    sns.barplot(
        x="Hour",
        y="Count",
        hue="Type",
        data=df_long,
        palette={"Departures": "skyblue", "Arrivals": "orange"},
    )
    plt.title("Avgångar & Ankomster per Timme (idag, 0..nu)", fontsize=16)
    plt.xlabel("Timme (0-23)", fontsize=14)
    plt.ylabel("Antal", fontsize=14)
    plt.legend(title="Typ")
    plt.tight_layout()

    return plt
