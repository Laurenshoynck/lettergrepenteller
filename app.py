from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/lettergrepen', methods=['POST'])
def lettergrepen():
    data = request.json
    naam = data.get('naam')

    from dotenv import load_dotenv
import os

load_dotenv()  # Laad de variabelen uit .env
openai.api_key = os.getenv("OPENAI_API_KEY")
    
    resultaat = {
        "naam": naam,
        "lettergrepen": 3,  # Voorbeeldwaarde
        "klemtoon": "eerste"
    }
    return jsonify(resultaat)

@app.route('/')
def home():
    return "Welkom bij de lettergrepenteller API. Gebruik /lettergrepen voor resultaten."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
