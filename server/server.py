from crypt import methods
from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': '*'}})

@app.route("/test")
def members(): 
	return {"test": ["test1", "test2", "test3"]}

@app.route("/backend", methods=['POST'])
def testingFile():
	print(request)
	data = request.get_json()
	print(data)
	return data


if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
	# app.run(debug=True)
