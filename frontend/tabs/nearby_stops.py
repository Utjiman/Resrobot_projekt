import streamlit as st
from streamlit.components.v1 import html

from backend.stops import Stops
from frontend.plot_maps import create_map_with_stops, get_nearby_stops


class NearbyStopsPage:
    def __init__(self, lang_texts, resrobot):
        self.lang_texts = lang_texts
        self.resrobot = resrobot
        self.stops = Stops(self.resrobot)

    def display_nearby_stops(self):
        """Sidan för närliggande hållplatser med kartvy."""
        st.markdown(f"# {self.lang_texts['nearby_header']}")
        st.markdown(self.lang_texts["nearby_description"])

        location_query = st.sidebar.text_input(
            self.lang_texts["enter_station"], key="station_search"
        )
        ext_id = None

        if location_query:
            results = self.stops.search_stop_by_name(location_query)
            if results:
                stop_options = {res["name"]: res["extId"] for res in results}
                selected_stop = st.sidebar.selectbox(
                    self.lang_texts["choose_stop"], list(stop_options.keys())
                )
                ext_id = stop_options[selected_stop]
            else:
                st.warning(self.lang_texts["no_stations_found"])

        radius = st.slider(
            self.lang_texts["radius_slider"],
            min_value=100,
            max_value=1000,
            step=100,
            value=500,
        )

        if ext_id:
            try:
                stops_data = get_nearby_stops(ext_id, radius=radius)
                folium_map = create_map_with_stops(stops_data)
                html(folium_map._repr_html_(), height=600)
            except Exception as e:
                st.error(f"Något gick fel: {e}")
        else:
            st.info(self.lang_texts["info_enter_stop"])
