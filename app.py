from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CLIENT_ID = 'dc2e9744-e001-47e4-b757-938267e4dacd'
REDIRECT_URI = 'https://reddydamodar415-debug.github.io'

@app.route('/')
def home():
    return 'Upstox Token Server Running ✅'

@app.route('/token', methods=['POST'])
def get_token():
    data = request.json
    code = data.get('code')
    secret = data.get('secret')

    if not code or not secret:
        return jsonify({'error': 'Missing code or secret'}), 400

    try:
        res = requests.post('https://api.upstox.com/v2/login/authorization/token', data={
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': secret,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        }, headers={'Content-Type': 'application/x-www-form-urlencoded'})

        result = res.json()
        if 'access_token' in result:
            return jsonify({'access_token': result['access_token']})
        else:
            return jsonify({'error': str(result)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
