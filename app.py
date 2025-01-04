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

    # Gebruik de juiste API-aanroep voor chat modellen
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Of een ander geschikt chat model
        messages=[{"role": "user", "content": f"Tel de lettergrepen van het woord {naam}."}],
        max_tokens=10  # Beperk het aantal tokens om onnodige lange reacties te vermijden
    )

    resultaat = response['choices'][0]['message']['content'].strip()

    return jsonify({"naam": naam, "resultaat": resultaat})

@app.route('/')
def home():
    return "Welkom bij de lettergrepenteller API. Gebruik /lettergrepen voor resultaten."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
