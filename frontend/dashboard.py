import streamlit as st
from Graphs import prepare_and_plot_graph
from streamlit.components.v1 import html

from backend.connect_to_api import ResRobot
from backend.helpers import get_video_as_base64, load_css
from backend.Stop_module import Stops
from backend.time_table import TimeTable
from backend.translate import LANGUAGES, get_translated_texts
from frontend.plot_maps import create_map_with_stops, get_nearby_stops

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


def tidtabell_page(lang_texts):
    """Sidan för att visa tidtabeller."""
    st.markdown(f"# {lang_texts['departure_header']}")
    st.markdown(lang_texts["departure_subheader"])

    st.sidebar.header(lang_texts["settings"])
    # Funktioner i sidomenyn (kommer alltid vara synliga)
    function_options = {
        lang_texts["function_departures"]: "show_departure",
        lang_texts["function_time_left"]: "show_time_to_departure",
        lang_texts["function_one_hour"]: "show_one_hour_ahead",
    }

    selected_function = st.sidebar.selectbox(
        lang_texts["function_select"], list(function_options.keys())
    )

    # Sökfält för att ange station (bara visa när användaren skriver något)
    location_query = st.sidebar.text_input(
        lang_texts["enter_station"], key="station_search"
    )

    station_id = None
    selected_stop = None

    if location_query:
        results = stops.search_stop_by_name(location_query)
        if results:
            stop_options = {res["name"]: res["extId"] for res in results}
            selected_stop = st.sidebar.selectbox(
                lang_texts["choose_stop"],
                list(stop_options.keys()),
            )
            station_id = stop_options[selected_stop]
        else:
            st.sidebar.warning(lang_texts["no_stations_found"])

    # Om en station är vald, visa resultat baserat på vald funktion
    if station_id and selected_stop:
        timetable = TimeTable(resrobot)

        if selected_function == lang_texts["function_departures"]:
            departures = timetable.show_departure_from_stop(station_id)

        elif selected_function == lang_texts["function_time_left"]:
            limit = st.sidebar.number_input(
                lang_texts["function_limit"], min_value=1, max_value=50, value=20
            )
            departures = timetable.show_time_to_departure(station_id, limit=limit)

        elif selected_function == lang_texts["function_one_hour"]:
            departures = timetable.show_one_hour_ahead(station_id)

        # Visa avgångar i en tabell
        st.subheader(f"{lang_texts['table_subheader']} {selected_stop}")
        if departures:
            st.table(departures)
        else:
            st.write(lang_texts["no_departures"])


def reseplanerare_page(lang_texts):
    """Sidan för reseplanering (fortfarande under utveckling)."""
    st.markdown(f"# {lang_texts['planner_header']}")
    st.markdown(lang_texts["planner_coming_soon"])


def närliggande_page(lang_texts):
    """Sidan för närliggande hållplatser med kartvy."""
    st.markdown(f"# {lang_texts['nearby_header']}")
    st.markdown(lang_texts["nearby_description"])

    location_query = st.sidebar.text_input(
        lang_texts["enter_station"], key="station_search"
    )
    ext_id = None

    if location_query:
        results = stops.search_stop_by_name(location_query)
        if results:
            stop_options = {res["name"]: res["extId"] for res in results}
            selected_stop = st.sidebar.selectbox(
                lang_texts["choose_stop"], list(stop_options.keys())
            )
            ext_id = stop_options[selected_stop]
        else:
            st.warning(lang_texts["no_stations_found"])

    radius = st.slider(
        lang_texts["radius_slider"], min_value=100, max_value=1000, step=100, value=500
    )

    if ext_id:
        try:
            stops_data = get_nearby_stops(ext_id, radius=radius)
            folium_map = create_map_with_stops(stops_data)
            html(folium_map._repr_html_(), height=600)
        except Exception as e:
            st.error(f"Något gick fel: {e}")
    else:
        st.info(lang_texts["info_enter_stop"])


def data_page(lang_texts):
    """Sidan för att visa graf med ankomster/avgångar."""
    st.markdown(f"# {lang_texts['data_header']}")
    st.markdown(lang_texts["data_description"])

    location_query = st.sidebar.text_input(
        lang_texts["enter_station"], key="station_search"
    )
    station_id = None

    if location_query:
        results = stops.search_stop_by_name(location_query)
        if results:
            stop_options = {res["name"]: res["extId"] for res in results}
            selected_station = st.sidebar.selectbox(
                lang_texts["choose_stop"], list(stop_options.keys())
            )
            station_id = stop_options[selected_station]
        else:
            st.sidebar.warning(lang_texts["no_data"])

    if station_id:
        plot = prepare_and_plot_graph(station_id)
        st.pyplot(plot)


def main():

    selected_language = st.sidebar.selectbox("🌍 Välj språk", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[selected_language]
    lang_texts = get_translated_texts(lang_code)

    st.sidebar.title(lang_texts["sidebar_title"])

    page = st.sidebar.radio(
        lang_texts["go_to_page"],
        [
            lang_texts["sidebar_option1"],
            lang_texts["sidebar_option2"],
            lang_texts["sidebar_option3"],
            lang_texts["sidebar_option4"],
        ],
    )

    if page == lang_texts["sidebar_option1"]:
        tidtabell_page(lang_texts)
    elif page == lang_texts["sidebar_option2"]:
        reseplanerare_page(lang_texts)
    elif page == lang_texts["sidebar_option3"]:
        närliggande_page(lang_texts)
    elif page == lang_texts["sidebar_option4"]:
        data_page(lang_texts)


if __name__ == "__main__":
    main()
