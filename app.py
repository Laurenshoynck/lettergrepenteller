import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json
from flask_cors import CORS
from unidecode import unidecode  # Verwijdert accenten
from waitress import serve  # Production server

# ✅ Laad API-sleutel uit .env bestand
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Flask-app instellen
app = Flask(__name__)
CORS(app)

# ✅ JSON-bestand met 17.000+ namen
JSON_BESTAND = "namen_database.json"

# ✅ Laden van JSON-lijst met optimalisatie
try:
    with open(JSON_BESTAND, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    
    # **Alle namen in JSON converteren naar lowercase**
    namen_data = {unidecode(k).strip().lower(): v for k, v in raw_data.items()}
    print(f"✅ JSON geladen: {len(namen_data)} namen in database.")
except Exception as e:
    print(f"⚠️ Fout bij het laden van de JSON: {e}")
    namen_data = {}  # Gebruik een lege dict als het laden mislukt

# ✅ TESTROUTE: Controleer of JSON correct geladen is
@app.route('/test-json', methods=['GET'])
def test_json():
    return jsonify({"namen": list(namen_data.keys())[:20]})  # Laat de eerste 20 namen zien

# ✅ HOOFDROUTE: Verwerk naam en geef lettergrepen + klemtoon
@app.route('/lettergrepen', methods=['POST'])
def lettergrepen():
    data = request.json
    naam = data.get('naam')

    if not naam:
        return jsonify({"error": "Geen naam opgegeven"}), 400

    # **Verwijder accenten en maak naam lowercase**
    naam = unidecode(naam).strip().lower()

    # 1️⃣ **Eerst checken of naam in JSON staat**
    if naam in namen_data:
        resultaat = namen_data[naam]
        print(f"✅ Naam '{naam}' gevonden in JSON: {resultaat}")
        return jsonify({"naam": naam, "resultaat": resultaat})

    # 2️⃣ **Naam niet gevonden? Vraag het aan GPT-4**
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

# ✅ HOMEPAGE
@app.route('/')
def home():
    return "Welkom bij de verbeterde lettergrepenteller API. Gebruik /lettergrepen voor resultaten."

# ✅ Start de server met `waitress` voor productie
if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
