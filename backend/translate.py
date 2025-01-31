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


def translate_text(text, lang_code):
    """
    Översätter en given text med Google Translate.
    Om översättning misslyckas returneras originaltexten.
    """
    try:
        return translator.translate(text, dest=lang_code).text
    except Exception:
        return text


def get_translated_texts(lang_code):
    """
    Returnerar en dictionary med översatta texter för hela dashboarden.
    Originalen är på svenska, men översätts dynamiskt med Google Translate.
    """
    # Originaltexter på svenska
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
        "planner_coming_soon": "Denna sida är under konstruktion. Kommer snart ...",
        "nearby_header": "Närliggande Hållplatser",
        "nearby_description": "Här visas en karta med närliggande hållplatser baserat på en vald huvudhållplats.",
        "radius_slider": "Välj radie (i meter)",
        "info_enter_stop": "Ange en hållplats för att visa närliggande hållplatser.",
        "data_header": "Grafvisning",
        "data_description": "Visualisering av avgångar och ankomster per timme.",
        "no_data": "Inga matchande stationer hittades.",
    }

    translated_texts = {}
    for key, original_text in texts_sv.items():
        # Översätt inte om användaren valt Svenska
        if lang_code == "sv":
            translated_texts[key] = original_text
        else:
            translated_texts[key] = translate_text(original_text, lang_code)

    return translated_texts
