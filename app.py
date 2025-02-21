import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json
from flask_cors import CORS
from unidecode import unidecode  # Verwijdert accenten voor consistente naamvergelijking
from functools import lru_cache  # Cache voor snelle zoekopdrachten

# Laad API-sleutel uit .env bestand
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Flask-app instellen
app = Flask(__name__)
CORS(app)

# 📂 **Laad de JSON-database in RAM**
JSON_BESTAND = "namen_database.json"

try:
    with open(JSON_BESTAND, "r", encoding="utf-8") as f:
        namen_data = json.load(f)
    print(f"✅ JSON geladen: {len(namen_data)} namen in database.")
except Exception as e:
    print(f"⚠️ Fout bij het laden van de JSON: {e}")
    namen_data = {}  # Gebruik een lege dict als het laden mislukt

# **✅ CACHING VOOR SNELLERE ZOEKFUNCTIE**
@lru_cache(maxsize=5000)  # Maximaal 5000 recente namen in cache
def get_syllables_from_json(naam):
    """ Haal lettergreepgegevens uit JSON-bestand, hoofdletter-onafhankelijk. """
    naam = unidecode(naam).strip().lower()
    return namen_data.get(naam, None)  # Geef None als naam niet bestaat


# 📌 **TESTROUTE:** Check of de JSON correct is geladen
@app.route('/test-json', methods=['GET'])
def test_json():
    return jsonify({"namen": list(namen_data.keys())[:10]})  # Laat eerste 10 namen zien


# 📌 **HOOFDROUTE:** Verwerk naam en geef lettergrepen + klemtoon
@app.route('/lettergrepen', methods=['POST'])
def lettergrepen():
    data = request.json
    naam = data.get('naam')

    if not naam:
        return jsonify({"error": "Geen naam opgegeven"}), 400

    # ✅ **Stap 1: Naam normaliseren (accents verwijderen, lowercase)**
    naam = unidecode(naam).strip().lower()

    # ✅ **Stap 2: Eerst checken of naam in JSON staat**
    resultaat = get_syllables_from_json(naam)
    if resultaat:
        print(f"✅ Naam '{naam}' gevonden in JSON: {resultaat}")
        return jsonify({"naam": naam, "resultaat": resultaat})

    # ✅ **Stap 3: Naam niet gevonden? Raadpleeg GPT-4**
    print(f"🔍 Naam '{naam}' niet gevonden, raadpleeg GPT-4...")

    prompt = (
        f"Bepaal het aantal lettergrepen en de klemtoonpositie voor de naam '{naam}'. "
        f"Geef het antwoord in het exacte formaat 'aantal-klemtoon' (bijv. '2-1' voor Laurens). "
        f"Geef alleen het antwoord en geen verdere uitleg."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )
        resultaat = response['choices'][0]['message']['content'].strip()
        print(f"🤖 GPT-4 resultaat voor '{naam}': {resultaat}")
        return jsonify({"naam": naam, "resultaat": resultaat})
    except Exception as e:
        print(f"❌ Fout bij OpenAI API: {e}")
        return jsonify({"error": "Fout bij het ophalen van lettergrepen"}), 500


# **HOMEPAGE**
@app.route('/')
def home():
    return "Welkom bij de verbeterde lettergrepenteller API. Gebruik /lettergrepen voor resultaten."


if __name__ == '__main__':
    from waitress import serve  # Snellere productie-server i.p.v. Flask ingebouwde server
    print("🚀 Server draait op poort 5000 met Waitress...")
    serve(app, host="0.0.0.0", port=5000)
