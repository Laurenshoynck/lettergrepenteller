
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/lettergrepen', methods=['POST'])
def lettergrepen():
    data = request.json
    naam = data.get('naam')
    resultaat = {
        "naam": naam,
        "lettergrepen": len(naam.split()),  # Example logic
        "klemtoon": "eerste"
    }
    return jsonify(resultaat)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
