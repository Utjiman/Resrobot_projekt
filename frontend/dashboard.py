import streamlit as st

from backend.connect_to_api import ResRobot
from backend.eda_visualization import prepare_and_plot_graph
from backend.time_table import TimeTable
from utils.constants import CSS_PATH, StationIds


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
    st.markdown("# Närliggande")
    st.markdown(
        "Denna sida är under konstruktion och kommer snart att erbjuda avancerade funktioner om närliggande hållplatser."
    )
    st.write("Kommer snart...")


def data_page():
    st.markdown("# Grafvisning")
    st.markdown("Visualisering av avgångar och ankomster per timme.")

    station_id = 740000002

    plot = prepare_and_plot_graph(station_id)
    st.pyplot(plot)


def main():
    st.set_page_config(page_title="Reseplanerare", layout="wide")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Gå till", ["Tidtabell", "Reseplanerare", "Närliggande", "Data"]
    )

    load_css()

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


def load_css():
    with open(CSS_PATH) as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
