from urllib import response
from flask import Flask
from flask import Flask, render_template, url_for, request, jsonify
from goatedData import mainFunction
from flask_cors import CORS, cross_origin

app = Flask(__name__)

@app.route('/createIndex', methods=['POST']) # ‘https://www.google.com/‘
@cross_origin(origins='*')
def home():
	try:
		print("hello world")
		data = request.get_json()
		returnData = mainFunction(data['address'], data['industry'], data['preferences'])
		print(returnData)
		return jsonify({
			'success' : True,
			'items': returnData
		})
	except Exception as e:
		print("ruh roh")
		print(e)
		return jsonify({
               'success': False,
               'items': []
		})
    
	

app.run(port=5000)