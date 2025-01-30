import os
import sys

import streamlit as st
from Graphs import prepare_and_plot_graph
from streamlit.components.v1 import html

from backend.connect_to_api import ResRobot
from backend.helpers import get_video_as_base64, load_css
from backend.Stop_module import Stops
from backend.time_table import TimeTable
from frontend.plot_maps import create_map_with_stops, get_nearby_stops

# Lägg till root-mappen i sys.path så att backend hittas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

resrobot = ResRobot()
stops = Stops(resrobot)
load_css("frontend/styles.css")

api_key = st.secrets["api"]["API_KEY"]

# Ladda in video som Base64
video_base64 = get_video_as_base64("frontend/media/2.mp4")

# Ladda in HTML-template för videon och ersätter platsen för Base64-värdet
with open("frontend/templates/banner.html", "r", encoding="utf-8") as f:
    banner_html = f.read().replace("{VIDEO_BASE64}", video_base64)

st.markdown(banner_html, unsafe_allow_html=True)


def tidtabell_page(timetable):
    st.markdown("# Tidtabell")
    st.markdown("Tidtabell för vald hållplats.")

    # Skapa instanser av ResRobot och Stops
    resrobot = ResRobot()
    stops = Stops(resrobot)

    st.sidebar.header("Inställningar")

    # Funktioner i sidomenyn (kommer alltid vara synliga)
    function_options = {
        "Visa avgångar från hållplats": "show_departure",
        "Visa tid kvar till avgång": "show_time_to_departure",
        "Visa avgångar inom en timme": "show_one_hour_ahead",
    }

    selected_function = st.sidebar.selectbox(
        "Välj funktion", list(function_options.keys())
    )

    # Sökfält för att ange station (bara visa när användaren skriver något)
    location_query = st.sidebar.text_input(
        "Ange en hållplats att söka efter:", key="station_search"
    )

    station_id = None  # Initiera station_id som None

    if location_query:
        # Sök efter stationer baserat på namn
        results = stops.search_stop_by_name(location_query)

        if results:
            # Skapa en dictionary med stationens namn och id
            stop_options = {res["name"]: res["extId"] for res in results}

            # Dynamisk dropdown baserat på sökresultat
            selected_stop = st.sidebar.selectbox(
                "Välj hållplats:",
                list(stop_options.keys()),
                index=(
                    0 if len(stop_options) > 0 else None
                ),  # Sätter standardval om resultat finns
            )

            # Hämta station_id från den valda stationen
            station_id = stop_options[selected_stop]
        else:
            st.sidebar.warning("Inga matchande hållplatser hittades.")

    # Om en station har valts, visa information för vald funktion
    if station_id:
        if selected_function == "Visa avgångar från hållplats":
            departures = timetable.show_departure_from_stop(station_id)

        elif selected_function == "Visa tid kvar till avgång":
            limit = st.sidebar.number_input(
                "Antal avgångar att visa", min_value=1, max_value=50, value=20
            )
            departures = timetable.show_time_to_departure(station_id, limit=limit)

        elif selected_function == "Visa avgångar inom en timme":
            departures = timetable.show_one_hour_ahead(station_id)

        # Visa avgångar
        st.subheader(f"Avgångar från {selected_stop}")
        if departures:
            st.table(departures)
        else:
            st.write("Inga avgångar hittades.")


def reseplanerare_page():
    st.markdown("# Reseplanerare")
    st.markdown(
        "Denna sida är under konstruktion och kommer snart att erbjuda avancerade reseplaneringsfunktioner."
    )
    st.write("Kommer snart...")


def närliggande_page():
    st.markdown("# Närliggande Hållplatser")
    st.markdown(
        "Här visas en karta med närliggande hållplatser baserat på en vald huvudhållplats."
    )

    # Inputfält för att ange en station (som kan användas med fuzzy search)
    location_query = st.sidebar.text_input(
        "Ange en hållplats att söka efter:", key="station_search"
    )

    # Skapa instanser av ResRobot och Stops för att kunna söka
    resrobot = ResRobot()
    stops = Stops(resrobot)

    # Hämta extId för vald hållplats om användaren skriver något i sökfältet
    ext_id = None
    if location_query:
        results = stops.search_stop_by_name(location_query)
        if results:
            stop_options = {res["name"]: res["extId"] for res in results}
            selected_stop = st.sidebar.selectbox(
                "Välj en hållplats:", list(stop_options.keys())
            )
            ext_id = stop_options[selected_stop]
        else:
            st.warning("Inga matchande hållplatser hittades.")

    # Radie för närliggande hållplatser
    radius = st.slider(
        "Välj radie (i meter)", min_value=100, max_value=1000, step=100, value=500
    )

    # Generera kartan om ext_id är angiven (eller använd det som valts)
    if ext_id:
        try:
            stops_data = get_nearby_stops(ext_id, radius=radius)
            folium_map = create_map_with_stops(stops_data)

            # Visa kartan i Streamlit
            html(folium_map._repr_html_(), height=600)
        except Exception as e:
            st.error(f"Något gick fel: {e}")
    else:
        st.info("Ange en hållplats för att visa närliggande hållplatser.")


def data_page():
    st.markdown("# Grafvisning")
    st.markdown("Visualisering av avgångar och ankomster per timme.")

    location_query = st.sidebar.text_input(
        "Ange en station att söka efter:", key="station_search"
    )

    station_id = None  # Initiera station_id som None

    if location_query:
        # Sök efter stationer baserat på namn
        results = stops.search_stop_by_name(location_query)

        if results:
            # Skapa en dictionary med stationens namn och id
            stop_options = {res["name"]: res["extId"] for res in results}

            # Dynamisk dropdown baserat på sökresultat
            selected_station = st.sidebar.selectbox(
                "Välj en station:",
                list(stop_options.keys()),
                index=(
                    0 if len(stop_options) > 0 else None
                ),  # Sätter standardval om resultat finns
            )

            # Hämta station_id från den valda stationen
            station_id = stop_options[selected_station]
        else:
            st.sidebar.warning("Inga matchande stationer hittades.")

    if station_id:
        # Kör visualisering om en station är vald
        plot = prepare_and_plot_graph(station_id)
        st.pyplot(plot)


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Gå till", ["Tidtabell", "Reseplanerare", "Närliggande", "Data"]
    )

    if page == "Tidtabell":
        # Instansiera ResRobot och TimeTable endast om Tidtabell-sidan väljs
        resrobot = ResRobot()
        timetable = TimeTable(resrobot)
        tidtabell_page(timetable)
    elif page == "Reseplanerare":
        reseplanerare_page()
    elif page == "Närliggande":
        närliggande_page()
    elif page == "Data":
        data_page()


if __name__ == "__main__":
    main()
