import openai
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_cors import CORS
from unidecode import unidecode  # Voor accenten verwijderen

# Load API key en Flask setup
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# 🔹 JSON-bestand inladen bij opstarten, zodat het niet telkens opnieuw hoeft.
with open("namen_database.json", "r", encoding="utf-8") as f:
    namen_data = json.load(f)

@app.route('/lettergrepen', methods=['POST'])
def lettergrepen():
    data = request.json
    naam = data.get('naam')

    if not naam:
        return jsonify({"error": "Geen naam opgegeven"}), 400

    # 🔹 Maak de naam lowercase en verwijder accenten voor een betere match
    naam_zoek = unidecode(naam.lower())

    # 🔹 Stap 1: Check of de naam in de JSON staat
    if naam_zoek in namen_data:
        resultaat = namen_data[naam_zoek]
        print(f"Naam gevonden in JSON: {naam_zoek} -> {resultaat}")
    else:
        # 🔹 Stap 2: Gebruik ChatGPT als backup
        print(f"Naam niet gevonden in JSON, opvragen bij GPT: {naam_zoek}")
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

        # ✅ Optioneel: Nieuw resultaat opslaan in JSON voor volgende keer
        namen_data[naam_zoek] = resultaat
        with open("namen_database.json", "w", encoding="utf-8") as f:
            json.dump(namen_data, f, indent=4)

    return jsonify({"naam": naam, "resultaat": resultaat})

@app.route('/')
def home():
    return "Welkom bij de verbeterde lettergrepenteller API. Gebruik /lettergrepen voor resultaten."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
