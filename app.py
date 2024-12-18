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

    # Nieuwe API-aanroep voor OpenAI versie >=1.0.0
    response = openai.completions.create(
        model="gpt-3.5-turbo",  # Kies een geschikt model, bijvoorbeeld gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "Je helpt bij het tellen van lettergrepen."},
            {"role": "user", "content": f"Tel de lettergrepen van het woord {naam}."}
        ]
    )

    resultaat = response['choices'][0]['message']['content'].strip()

    return jsonify({"naam": naam, "resultaat": resultaat})

@app.route('/')
def home():
    return "Welkom bij de lettergrepenteller API. Gebruik /lettergrepen voor resultaten."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

