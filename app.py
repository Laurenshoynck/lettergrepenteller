from flask import Flask, request, jsonify
import openai
import os
import re

app = Flask(__name__)

# Gebruik de omgevingsvariabele direct zonder .env bestand
openai.api_key = os.environ.get("OPENAI_API_KEY")  # Render haalt deze sleutel op

# Functie om het aantal lettergrepen te tellen
def count_syllables(word):
    word = word.lower()
    syllables = re.findall(r'[aeiouy]+', word)
    return len(syllables)

# Route voor de lettergrepen API
@app.route('/lettergrepen', methods=['POST'])
def lettergrepen():
    data = request.json
    naam = data.get('naam')

    # Aantal lettergrepen zelf berekenen
    num_syllables = count_syllables(naam)

    # Vraag GPT-3 om de klemtoon te berekenen
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Geef de klemtoon van het woord '{naam}'.",
        max_tokens=50
    )
    klemtoon = response.choices[0].text.strip()

    resultaat = {
        "naam": naam,
        "lettergrepen": num_syllables,
        "klemtoon": klemtoon
    }

    return jsonify(resultaat)

# Route voor de homepagina
@app.route('/')
def home():
    return "Welkom bij de lettergrepenteller API. Gebruik /lettergrepen voor resultaten."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

