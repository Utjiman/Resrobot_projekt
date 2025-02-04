from functools import lru_cache

from googletrans import Translator

LANGUAGES = {
    "Svenska": "sv",
    "English": "en",
    "Suomi": "fi",
    "Dansk": "da",
    "Deutsch": "de",
    "Français": "fr",
    "Español": "es",
    "中文 (Zhōngwén)": "zh-cn",
    "Русский (Russkiy)": "ru",
}

translator = Translator()


@lru_cache(maxsize=128)
def translate_text(text, lang_code):
    """
    Översätter en given text med Google Translate.
    Om översättning misslyckas returneras originaltexten.
    """
    try:
        translated = translator.translate(text, dest=lang_code)
        return translated.text
    except Exception as e:
        print(f"Translation error for '{text}' to '{lang_code}': {e}")
        return text


def get_translated_texts(lang_code):
    """
    Returnerar en dictionary med översatta texter för hela dashboarden.
    Originaltexterna är på svenska, men översätts dynamiskt med Google Translate.
    """
    texts_sv = {
        "choose_language": "🌍 Välj språk",
        "sidebar_title": "Navigation",
        "go_to_page": "Gå till",
        "sidebar_option1": "Tidtabell",
        "sidebar_option2": "Reseplanerare",
        "sidebar_option3": "Närliggande",
        "sidebar_option4": "Data",
        "settings": "Inställningar",
        "function_select": "Välj funktion",
        "function_departures": "Visa avgångar från hållplats",
        "function_time_left": "Visa tid kvar till avgång",
        "function_one_hour": "Visa avgångar inom en timme",
        "function_limit": "Antal avgångar att visa",
        "departures": "Avgångar från",
        "no_departures": "Inga avgångar hittades.",
        "no_stations_found": "Inga matchande hållplatser hittades.",
        "enter_station": "Ange en hållplats att söka efter:",
        "choose_stop": "Välj en hållplats:",
        "departure_header": "Tidtabell",
        "departure_subheader": "Tidtabell för vald hållplats.",
        "table_subheader": "Avgångar från",
        "planner_header": "Reseplanerare",
        "planner_choose_trip": "Välj en resa för att visa information och karta:",
        "planner_no_trips": "Inga fler resor tillgängliga idag.",
        "planner_trip_not_found": "Ingen resa hittades mellan de valda stationerna.",
        "planner_trip_error": "Ett fel uppstod vid hämtning av resedata: ",
        "planner_origin": "Ange startstation:",
        "planner_destination": "Ange destination:",
        "planner_select_origin": "Välj startstation:",
        "planner_select_destination": "Välj destination:",
        "planner_select_trip": "Välj resa:",
        "planner_trip_info": "Reseinformation",
        "planner_total_stops": "🛑 Antal hållplatser",
        "planner_total_changes": "🔄 Byten",
        "planner_total_time": "⏳ Total restid",
        "planner_no_map": "Ingen karta kunde genereras för denna resa.",
        "insufficient_data_map": "Det finns inte tillräckligt med data för att generera karta.",
        "nearby_header": "Närliggande Hållplatser",
        "nearby_description": "Här visas en karta med närliggande hållplatser baserat på en vald huvudhållplats.",
        "radius_slider": "Välj radie (i meter)",
        "info_enter_stop": "Ange en hållplats för att visa närliggande hållplatser.",
        "data_header": "Grafvisning",
        "data_description": "Visualisering av avgångar och ankomster per timme.",
        "no_data": "Inga matchande stationer hittades.",
        "planner_sidebar_title": "🚆 Reseplanering",
        "toggle_show": "Visa fler stationer",
        "toggle_hide": "Visa färre stationer",
        "info_enter_station": "Vänligen ange både startstation och destination för att planera din resa.",
    }
    translated_texts = {}
    for key, original_text in texts_sv.items():
        if lang_code == "sv":
            translated_texts[key] = original_text
        else:
            translated_texts[key] = translate_text(original_text, lang_code)
    return translated_texts
