import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from backend.resrobot_day import ResRobotDay

# Lägg till projektroten i sökvägen så att backend hittas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


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
