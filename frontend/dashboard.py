import streamlit as st
from Graphs import prepare_and_plot_graph
from streamlit.components.v1 import html

from backend.connect_to_api import ResRobot
from backend.helpers import get_video_as_base64, load_css
from backend.Stop_module import Stops
from backend.translate import LANGUAGES, get_translated_texts
from frontend.plot_maps import create_map_with_stops, get_nearby_stops
from frontend.tabs.timetable import TimetablePage
from frontend.tabs.travel_planner import TravelPlannerPage

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
    # SwedenToGo
    selected_language = st.sidebar.selectbox("🌍 Välj språk", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[selected_language]
    lang_texts = get_translated_texts(lang_code)

    st.sidebar.title(lang_texts["sidebar_title"])

    timetable = TimetablePage(lang_texts=lang_texts, resrobot=resrobot)
    travel_planner = TravelPlannerPage(lang_texts=lang_texts, resrobot=resrobot)

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
        timetable.display_timetable()
    elif page == lang_texts["sidebar_option2"]:
        travel_planner.display_travel_planner()
    elif page == lang_texts["sidebar_option3"]:
        närliggande_page(lang_texts)
    elif page == lang_texts["sidebar_option4"]:
        data_page(lang_texts)


if __name__ == "__main__":
    main()
