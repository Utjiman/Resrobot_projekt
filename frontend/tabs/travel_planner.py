import os

import streamlit as st

from backend.Stop_module import Stops
from backend.trips import TripPlanner


class TravelPlannerPage:
    def __init__(self, lang_texts, resrobot):
        self.lang_texts = lang_texts
        self.resrobot = resrobot
        self.stops = Stops(self.resrobot)

    def display_travel_planner(self):
        st.markdown(f"# {self.lang_texts['planner_header']}")
        st.sidebar.subheader(self.lang_texts["planner_sidebar_title"])

        origin_input = st.sidebar.text_input(
            self.lang_texts["planner_origin"], key="origin_search"
        )
        destination_input = st.sidebar.text_input(
            self.lang_texts["planner_destination"], key="destination_search"
        )

        if not origin_input or not destination_input:
            st.info(
                "Vänligen ange både startstation och destination för att planera din resa."
            )
            return

        origin_id, destination_id = None, None

        results_origin = self.stops.search_stop_by_name(origin_input)
        if results_origin:
            origin_options = {res["name"]: res["extId"] for res in results_origin}
            selected_origin = st.sidebar.selectbox(
                self.lang_texts["planner_select_origin"], list(origin_options.keys())
            )
            origin_id = origin_options[selected_origin]
        else:
            st.warning(
                "Inga resultat för startstationen, kontrollera stavningen eller försök med en annan station."
            )

        results_destination = self.stops.search_stop_by_name(destination_input)
        if results_destination:
            destination_options = {
                res["name"]: res["extId"] for res in results_destination
            }
            selected_destination = st.sidebar.selectbox(
                self.lang_texts["planner_select_destination"],
                list(destination_options.keys()),
            )
            destination_id = destination_options[selected_destination]
        else:
            st.warning(
                "Inga resultat för destinationen, kontrollera stavningen eller försök med en annan station."
            )

        if origin_id and destination_id:
            trip_planner = TripPlanner(origin_id, destination_id)
            try:
                trips_today = trip_planner.next_available_trips_today()
                if trips_today:
                    st.subheader(self.lang_texts["planner_choose_trip"])

                    selected_trip_index = st.selectbox(
                        self.lang_texts["planner_select_trip"],
                        options=list(range(len(trips_today))),
                        format_func=lambda i: f"Resa {i+1} - {trips_today[i]['time'].iloc[0]} ({trips_today[i]['date'].iloc[0]})",
                    )
                    df_trip = trips_today[selected_trip_index]
                    if df_trip is not None and not df_trip.empty:
                        st.subheader(self.lang_texts["planner_trip_info"])

                        # Konvertera DataFrame till HTML med klassen "my-travel-table"
                        table_html = df_trip[["name", "time", "date"]].to_html(
                            classes="my-travel-table",
                            index=False,
                            header=False,
                            border=0,
                        )

                        template_path = os.path.join(
                            "frontend", "templates", "res_info.html"
                        )
                        with open(template_path, "r", encoding="utf-8") as file:
                            html_template = file.read()

                        res_info_html = html_template.replace(
                            "{{ table_content }}", table_html
                        )

                        # Visa den sammansatta HTML-koden
                        st.markdown(res_info_html, unsafe_allow_html=True)

                        # Visa övriga metrik med kolumner
                        col1, col2, col3 = st.columns(3)
                        col1.metric(
                            self.lang_texts["planner_total_stops"],
                            trip_planner.calc_number_of_stops(
                                trip_index=selected_trip_index
                            ),
                        )
                        col2.metric(
                            self.lang_texts["planner_total_changes"],
                            trip_planner.calc_number_of_changes(
                                trip_index=selected_trip_index
                            ),
                        )
                        col3.metric(
                            self.lang_texts["planner_total_time"],
                            trip_planner.calc_total_time(
                                trip_index=selected_trip_index
                            ),
                        )

                        trip_map = trip_planner.map_for_trip(
                            trip_index=selected_trip_index
                        )
                        if trip_map:
                            st.components.v1.html(trip_map._repr_html_(), height=500)
                        else:
                            st.warning(self.lang_texts["planner_no_map"])
                    else:
                        st.warning(self.lang_texts["planner_trip_not_found"])
                else:
                    st.warning(self.lang_texts["planner_no_trips"])
            except Exception as e:
                st.error(f"{self.lang_texts['planner_trip_error']} {e}")
        else:
            st.info("Vänligen ange både start och destination för att visa resor.")
