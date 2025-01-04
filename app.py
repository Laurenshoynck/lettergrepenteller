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
        messages=[{"role": "user", "content": f"This GPT is designed to assist Shopify users by analyzing names entered by customers, providing the number of syllables in each name, and indicating the stressed syllable for proper pronunciation. It aims to enhance user engagement and personalization within a Shopify store environment by quickly and accurately processing name input and delivering syllable counts and stress patterns."}],
        max_tokens=10  # Beperk het aantal tokens om onnodige lange reacties te vermijden
    )

    resultaat = response['choices'][0]['message']['content'].strip()

    return jsonify({"naam": naam, "resultaat": resultaat})

@app.route('/')
def home():
    return "Welkom bij de lettergrepenteller API. Gebruik /lettergrepen voor resultaten."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
