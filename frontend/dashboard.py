import streamlit as st
import streamlit.components.v1 as components
from Graphs import prepare_and_plot_graph

from backend.connect_to_api import ResRobot
from backend.helpers import get_video_as_base64, load_css
from backend.time_table import TimeTable
from frontend.plot_maps import create_map_with_stops, get_nearby_stops
from utils.constants import StationIds

load_css("frontend/styles.css")

# Ladda in video som Base64
video_base64 = get_video_as_base64("frontend/media/2.mp4")

# Ladda in HTML-template för videon och ersätter platsen för Base64-värdet
with open("frontend/templates/banner.html", "r", encoding="utf-8") as f:
    banner_html = f.read().replace("{VIDEO_BASE64}", video_base64)

st.markdown(banner_html, unsafe_allow_html=True)


def tidtabell_page(timetable):
    st.markdown("# Tidtabell")
    st.markdown("Tidtabell för vald hållplats.")
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

    ext_id = st.text_input("Ange extId för huvudhållplats", value="740001590")

    # Radie för närliggande hållplatser
    radius = st.slider(
        "Välj radie (i meter)", min_value=100, max_value=1000, step=100, value=500
    )

    # Generera kartan om ext_id är angiven
    if ext_id:
        try:
            stops_data = get_nearby_stops(ext_id, radius=radius)
            folium_map = create_map_with_stops(stops_data)

            # Visa kartan i Streamlit
            components.html(folium_map._repr_html_(), height=600)
        except Exception as e:
            st.error(f"Något gick fel: {e}")
    else:
        st.info("Ange en extId för att visa hållplatser.")


def data_page():
    st.markdown("# Grafvisning")
    st.markdown("Visualisering av avgångar och ankomster per timme.")

    station_id = 740000002

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
