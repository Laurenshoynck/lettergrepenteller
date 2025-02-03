import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_cors import CORS  # Importeer CORS

load_dotenv()  # Laad de variabelen uit .env
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Schakel CORS in

@app.route('/lettergrepen', methods=['POST'])
def lettergrepen():
    data = request.json
    naam = data.get('naam')

    if not naam:
        return jsonify({"error": "Geen naam opgegeven"}), 400

    # Verbeterde prompt voor nauwkeurigere lettergreep- en klemtoonbepaling
    prompt = (
        f"Bepaal het aantal lettergrepen en de klemtoonpositie voor de naam '{naam}'. "
        f"Houd rekening met de natuurlijke uitspraak zoals een moedertaalspreker dat zou doen. "
        f"Bepaal de meest gangbare uitspraak en markeer de klemtoon op de meest logische lettergreep. "
        f"Geef het antwoord in het exacte formaat 'aantal-klemtoon' (bijv. '2-1' voor Laurens of '3-2' voor Roswitha). "
        f"Geef alleen het antwoord en geen verdere uitleg."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Gebruik GPT-4 voor betere taalverwerking
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10  # Iets ruimer om een compleet antwoord te krijgen
    )

    resultaat = response['choices'][0]['message']['content'].strip()

    return jsonify({"naam": naam, "resultaat": resultaat})

@app.route('/')
def home():
    return "Welkom bij de verbeterde lettergrepenteller API. Gebruik /lettergrepen voor resultaten."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
