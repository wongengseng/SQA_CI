from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello, World!", "status": "success"})

@app.route('/health')
def health():
    # Simulate occasional health check failures
    if random.random() < 0.1:  # 10% failure rate
        return jsonify({"status": "unhealthy"}), 503
    return jsonify({"status": "healthy"}), 200

@app.route('/api/data')
def get_data():
    data = {
        "users": 150,
        "active_sessions": 42,
        "uptime_percentage": 99.9
    }
    return jsonify(data)

@app.route('/api/calculate/<int:num>')
def calculate(num):
    result = num * 2 + 10
    return jsonify({"input": num, "result": result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
