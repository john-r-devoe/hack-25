from flask import Flask

app = Flask(__name__)

@app.route('/') # ‘https://www.google.com/‘

def home():
	return "Hello, world!"

app.run(port=5000)