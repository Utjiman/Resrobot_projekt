import streamlit as st
from Graphs import prepare_and_plot_graph

from backend.Stop_module import Stops


class DataPage:
    """
    A Streamlit page for displaying public transport data.

    This class provides a user interface for searching transport stops
    and visualizing arrival and departure data in a graph.

    Features:
    - Search for transport stops by name.
    - Select a stop from search results.
    - Display a graph of arrivals and departures.
    """

    def __init__(self, lang_texts, resrobot):
        self.lang_texts = lang_texts
        self.resrobot = resrobot
        self.stops = Stops(self.resrobot)

    def display_data(self):
        """Sidan för att visa graf med ankomster/avgångar."""
        st.markdown(f"# {self.lang_texts['data_header']}")
        st.markdown(self.lang_texts["data_description"])

        location_query = st.sidebar.text_input(
            self.lang_texts["enter_station"], key="station_search"
        )
        station_id = None

        if location_query:
            results = self.stops.search_stop_by_name(location_query)
            if results:
                stop_options = {res["name"]: res["extId"] for res in results}
                selected_station = st.sidebar.selectbox(
                    self.lang_texts["choose_stop"], list(stop_options.keys())
                )
                station_id = stop_options[selected_station]
            else:
                st.sidebar.warning(self.lang_texts["no_data"])

        if station_id:
            plot = prepare_and_plot_graph(station_id)
            st.pyplot(plot)
