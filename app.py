import openai
import json
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from unidecode import unidecode  # Verwijdert accenten voor consistente naamvergelijking

# 🔹 Laad omgevingsvariabelen en OpenAI API-key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# 🔹 JSON-bestand inlezen
JSON_FILE = "namen_database.json"

def load_namen_data():
    """Laad de naam-database uit JSON en print het aantal namen"""
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"📂 JSON geladen: {len(data)} namen in database.")  # 🔹 Debugging log
            return data
    except FileNotFoundError:
        print("⚠️  JSON-bestand niet gevonden! Een nieuw bestand wordt aangemaakt.")
        return {}
    except json.JSONDecodeError:
        print("⚠️  JSON-bestand bevat fouten! Het wordt opnieuw geformatteerd.")
        return {}

namen_data = load_namen_data()  # Laden bij opstarten

@app.route('/lettergrepen', methods=['POST'])
def lettergrepen():
    data = request.json
    naam = data.get('naam')

    if not naam:
        return jsonify({"error": "Geen naam opgegeven"}), 400

    # 🔹 Naam normaliseren (kleine letters en accenten verwijderen)
    naam_zoek = unidecode(naam.strip().lower())

    print(f"🔍 Opgevraagde naam: '{naam_zoek}'")

    # 🔹 Debugging: Print alle namen in JSON
    print(f"📜 JSON bevat de volgende namen: {list(namen_data.keys())[:10]}...")

    # 🔹 Stap 1: Check of de naam in de JSON staat
    if naam_zoek in namen_data:
        resultaat = namen_data[naam_zoek]
        print(f"✅ Naam gevonden in JSON: {naam_zoek} -> {resultaat}")
    else:
        # 🔹 Stap 2: Naam niet gevonden, vraag GPT om hulp
        print(f"❌ Naam niet in JSON, opvragen bij GPT: {naam_zoek}")

        prompt = (
            f"Bepaal het aantal lettergrepen en de klemtoonpositie voor de naam '{naam}'. "
            f"Geef het antwoord in het exacte formaat 'aantal-klemtoon' (bijv. '2-1' voor Laurens of '3-2' voor Roswitha). "
            f"Geef alleen het antwoord en geen verdere uitleg."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )

        resultaat = response['choices'][0]['message']['content'].strip()

        # ✅ Opslaan in JSON-bestand zodat GPT niet opnieuw wordt aangeroepen
        namen_data[naam_zoek] = resultaat
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(namen_data, f, indent=4)

        print(f"📝 Nieuwe naam toegevoegd aan JSON: {naam_zoek} -> {resultaat}")

    return jsonify({"naam": naam, "resultaat": resultaat})

@app.route('/')
def home():
    return "Welkom bij de verbeterde lettergrepenteller API. Gebruik /lettergrepen voor resultaten."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
