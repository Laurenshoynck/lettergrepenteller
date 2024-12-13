from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/lettergrepen', methods=['POST'])
def lettergrepen():
    data = request.json
    naam = data.get('naam')
   openai.api_key = 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
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
