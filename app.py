import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json
from flask_cors import CORS  # Importeer CORS
from unidecode import unidecode  # Verwijdert accenten voor consistente naamvergelijking

load_dotenv()  # Laad de variabelen uit .env
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Schakel CORS in

# Laad de namen database (zorg dat het bestand op dezelfde locatie staat als app.py)
with open("namen_database.json", "r", encoding="utf-8") as file:
    namen_database = json.load(file)

@app.route('/lettergrepen', methods=['POST'])
def lettergrepen():
    data = request.json
    naam = data.get('naam')

    if not naam:
        return jsonify({"error": "Geen naam opgegeven"}), 400

    # Verwijder accenten en zet naam om naar lowercase voor een consistente vergelijking
    naam_normaal = unidecode(naam).lower()

    # **Stap 1: Controleer eerst of naam al in JSON staat**
    if naam_normaal in namen_database:
        resultaat = namen_database[naam_normaal]
        print(f"✅ Naam gevonden in JSON: {naam} → {resultaat}")
        return jsonify({"naam": naam, "resultaat": resultaat})

    # **Stap 2: Als naam niet in JSON staat, gebruik GPT**
    print(f"⚠️ Naam niet gevonden, vraag GPT om hulp: {naam}")
    prompt = (
        f"Bepaal het aantal lettergrepen en de klemtoonpositie voor de naam '{naam}'. "
        f"Geef het antwoord in het exacte formaat 'aantal-klemtoon' (bijv. '2-1' voor Laurens). "
        f"Geef alleen het antwoord en geen verdere uitleg."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",  
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10  
    )

    resultaat = response['choices'][0]['message']['content'].strip()

    return jsonify({"naam": naam, "resultaat": resultaat})

@app.route('/')
def home():
    return "Welkom bij de verbeterde lettergrepenteller API. Gebruik /lettergrepen voor resultaten."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
