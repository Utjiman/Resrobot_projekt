import streamlit as st

from backend.stop_module import Stops
from backend.timetable import TimeTable


class TimetablePage:
    """
    A Streamlit page for displaying public transport timetables.

    This class allows users to search for a transport stop, select a function
    to display different timetable views, and view upcoming departures in a table.

    Features:
    - Search for transport stops by name.
    - Select different timetable functions (departures, time left, one hour ahead).
    - Display departure data in a structured table.
    """

    def __init__(self, lang_texts, resrobot):
        self.lang_texts = lang_texts
        self.resrobot = resrobot
        self.stops = Stops(self.resrobot)

    def display_timetable(self):

        st.markdown(f"# {self.lang_texts['departure_header']}")
        st.markdown(self.lang_texts["departure_subheader"])

        st.sidebar.header(self.lang_texts["settings"])

        location_query = st.sidebar.text_input(
            self.lang_texts["enter_station"], key="station_search"
        )

        function_options = {
            self.lang_texts["function_departures"]: "show_departure",
            self.lang_texts["function_time_left"]: "show_time_to_departure",
            self.lang_texts["function_one_hour"]: "show_one_hour_ahead",
        }

        selected_function = st.sidebar.selectbox(
            self.lang_texts["function_select"], list(function_options.keys())
        )

        station_id = None
        selected_stop = None

        if location_query:
            results = self.stops.search_stop_by_name(location_query)
            if results:
                stop_options = {res["name"]: res["extId"] for res in results}
                selected_stop = st.sidebar.selectbox(
                    self.lang_texts["choose_stop"],
                    list(stop_options.keys()),
                )
                station_id = stop_options[selected_stop]
            else:
                st.sidebar.warning(self.lang_texts["no_stations_found"])

        if station_id and selected_stop:
            timetable = TimeTable(self.resrobot)

            if selected_function == self.lang_texts["function_departures"]:
                departures = timetable.show_departure_from_stop(station_id)

            elif selected_function == self.lang_texts["function_time_left"]:
                limit = st.sidebar.number_input(
                    self.lang_texts["function_limit"],
                    min_value=1,
                    max_value=50,
                    value=20,
                )
                departures = timetable.show_time_to_departure(station_id, limit=limit)

            elif selected_function == self.lang_texts["function_one_hour"]:
                departures = timetable.show_one_hour_ahead(station_id)

            st.subheader(f"{self.lang_texts['table_subheader']} {selected_stop}")
            if departures:
                st.table(departures)
            else:
                st.write(self.lang_texts["no_departures"])
