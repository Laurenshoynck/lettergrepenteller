import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()  # Laad de variabelen uit .env
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/lettergrepen', methods=['POST'])
def lettergrepen():
    data = request.json
    naam = data.get('naam')

    if not naam:
        return jsonify({"error": "Geen naam opgegeven"}), 400

    # Prompt om direct het aantal lettergrepen en de klemtoonpositie terug te geven
    prompt = f"Bepaal het aantal lettergrepen en de klemtoonpositie voor de naam '{naam}'. " \
             f"Geef het antwoord in het exacte formaat 'aantal-klemtoon' (bijv. '2-1' voor Laurens). " \
             f"Geef alleen het antwoord en geen verdere uitleg."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Of een ander geschikt model zoals gpt-4
        messages=[{"role": "user", "content": prompt}],
        max_tokens=5  # Beperkt tot alleen het antwoord
    )

    resultaat = response['choices'][0]['message']['content'].strip()

    return jsonify({"naam": naam, "resultaat": resultaat})

@app.route('/')
def home():
    return "Welkom bij de lettergrepenteller API. Gebruik /lettergrepen voor resultaten."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
