import streamlit as st

from backend.connect_to_api import ResRobot
from backend.helpers import get_video_as_base64, load_css
from backend.translate import LANGUAGES, get_translated_texts
from frontend.tabs.data import DataPage
from frontend.tabs.nearby_stops import NearbyStopsPage
from frontend.tabs.timetable import TimetablePage
from frontend.tabs.travel_planner import TravelPlannerPage

resrobot = ResRobot()

load_css("frontend/styles.css")

api_key = st.secrets["api"]["API_KEY"]


video_base64 = get_video_as_base64("frontend/media/2.mp4")


with open("frontend/templates/banner.html", "r", encoding="utf-8") as f:
    banner_html = f.read().replace("{VIDEO_BASE64}", video_base64)

st.markdown(banner_html, unsafe_allow_html=True)


def main():
    st.sidebar.title("Sweden ToGo")

    selected_language = st.sidebar.selectbox("🌍 Välj språk", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[selected_language]
    lang_texts = get_translated_texts(lang_code)

    st.sidebar.title(lang_texts["sidebar_title"])

    data = DataPage(lang_texts=lang_texts, resrobot=resrobot)
    timetable = TimetablePage(lang_texts=lang_texts, resrobot=resrobot)
    travel_planner = TravelPlannerPage(lang_texts=lang_texts, resrobot=resrobot)
    nearby_stops = NearbyStopsPage(lang_texts=lang_texts, resrobot=resrobot)

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
        nearby_stops.display_nearby_stops()
    elif page == lang_texts["sidebar_option4"]:
        data.display_data()


if __name__ == "__main__":
    main()
