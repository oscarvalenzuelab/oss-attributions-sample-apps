from flask import Flask, request
import yaml
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Vulnerable Python App!"

@app.route('/fetch', methods=['POST'])
def fetch_data():
    url = request.form.get('url')
    response = requests.get(url)
    return response.text

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    data = yaml.safe_load(file)
    return f"Received data: {data}"

if __name__ == '__main__':
    app.run(debug=True)

