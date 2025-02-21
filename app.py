import json
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_cors import CORS  # Importeer CORS

load_dotenv()  # Laad de variabelen uit .env
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Schakel CORS in

# **Laad de namen-database in**
DATABASE_PATH = "namen_database.json"

def load_database():
    """ Laadt de namen en lettergrepen uit de JSON-database. """
    try:
        with open(DATABASE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("⚠️ Waarschuwing: namen_database.json niet gevonden!")
        return {}

namen_database = load_database()

@app.route('/lettergrepen', methods=['POST'])
def lettergrepen():
    data = request.json
    naam = data.get('naam').lower()  # Maak naam lowercase voor consistente zoekopdrachten

    if not naam:
        return jsonify({"error": "Geen naam opgegeven"}), 400

    # **STAP 1: Zoek de naam eerst in de database**
    if naam in namen_database:
        resultaat = namen_database[naam]
        return jsonify({"naam": naam, "resultaat": resultaat, "bron": "database"})

    # **STAP 2: Als naam niet in database staat, gebruik OpenAI**
    prompt = (
        f"Bepaal het aantal lettergrepen en de klemtoonpositie voor de naam '{naam}'. "
        f"Houd rekening met de natuurlijke uitspraak zoals een moedertaalspreker dat zou doen. "
        f"Bepaal de meest gangbare uitspraak en markeer de klemtoon op de meest logische lettergreep. "
        f"Geef het antwoord in het exacte formaat 'aantal-klemtoon' (bijv. '2-1' voor Laurens of '3-2' voor Roswitha). "
        f"Geef alleen het antwoord en geen verdere uitleg."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",  
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10  
    )

    resultaat = response['choices'][0]['message']['content'].strip()

    # **STAP 3: Sla het nieuwe resultaat op in de database**
    namen_database[naam] = resultaat
    with open(DATABASE_PATH, "w", encoding="utf-8") as file:
        json.dump(namen_database, file, ensure_ascii=False, indent=4)

    return jsonify({"naam": naam, "resultaat": resultaat, "bron": "AI"})


@app.route('/')
def home():
    return "Welkom bij de verbeterde lettergrepenteller API. Gebruik /lettergrepen voor resultaten."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
