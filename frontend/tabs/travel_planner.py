import streamlit as st

from backend.connect_to_api import ResRobot
from backend.Stop_module import Stops


class TravelPlannerPage:
    def __init__(self, lang_texts, resrobot):
        self.lang_texts = lang_texts
        self.resrobot = ResRobot()
        self.stops = Stops(resrobot)

    def display_travel_planner(self):
        """Sidan för reseplanering (fortfarande under utveckling)."""
        st.markdown(f"# {self.lang_texts['planner_header']}")
        st.markdown(self.lang_texts["planner_coming_soon"])
