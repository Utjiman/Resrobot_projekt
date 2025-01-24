import streamlit as st

from backend.connect_to_api import ResRobot
from backend.time_table import TimeTable
from utils.constants import StationIds


def main():
    st.set_page_config(page_title="Reseplanerare", layout="wide")
    st.markdown("# Tidtabell")
    st.markdown("Tidtabell för vald hållplats.")

    resrobot = ResRobot()
    timetable = TimeTable(resrobot)

    st.sidebar.header("Inställningar")
    stop_options = {station.name: station.value for station in StationIds}
    selected_stop = st.sidebar.selectbox("Välj hållplats", list(stop_options.keys()))
    stop_id = stop_options[selected_stop]

    # Funktioner i sidomenyn
    function_options = {
        "Visa avgångar från hållplats": "show_departure",
        "Visa tid kvar till avgång": "show_time_to_departure",
        "Visa avgångar inom en timme": "show_one_hour_ahead",
    }
    selected_function = st.sidebar.selectbox(
        "Välj funktion", list(function_options.keys())
    )

    if selected_function == "Visa avgångar från hållplats":
        departures = timetable.show_departure_from_stop(stop_id)

    elif selected_function == "Visa tid kvar till avgång":
        limit = st.sidebar.number_input(
            "Antal avgångar att visa", min_value=1, max_value=50, value=20
        )
        departures = timetable.show_time_to_departure(stop_id, limit=limit)

    elif selected_function == "Visa avgångar inom en timme":
        departures = timetable.show_one_hour_ahead(stop_id)

    st.subheader(f"Avgångar från {selected_stop}")
    if departures:
        st.table(departures)
    else:
        st.write("Inga avgångar hittades.")


if __name__ == "__main__":
    main()
