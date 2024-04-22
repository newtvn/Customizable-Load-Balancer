from flask import Flask, jsonify # type: ignore
import os

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home():
    server_id = os.environ.get('SERVER_ID', '1')
    return jsonify(message=f"Hello from Server: {server_id}", status="successful"), 200

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)